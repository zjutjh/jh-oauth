from django.http import HttpRequest, HttpResponse, JsonResponse, Http404
import json

from oauth import extensions
from . import tool
from ..extensions import config, get_ip
from ..models import AppScheme, User, UserActivity
from ..apis import jh_user
from ..consts import SHORTCUT
import logging


def login(request: HttpRequest):
    """
    用户的登录操作，不包含oauth中的登录操作
    :param request:
    :return:
    """
    # region 获取参数
    args = tool.get_args(request)
    if args is None:
        return Http404()
    try:
        name = tool.check_name(args['name'])
        password = tool.check_password(args['password'])
        device_type = tool.check_device_type(args['device_type'])
    except KeyError:
        return tool.create_res_template(SHORTCUT.AE)
    except ValueError as e:
        return tool.create_res_afe(e.args[0])
    try:
        token = tool.check_token(args.get('token', None))
    except ValueError as e:
        return tool.create_res_afe(e.args[0])
    access_id = None
    if token is not None:
        token_raw = extensions.decrypt_token(token)
        if token_raw is None:
            return tool.create_res_template(SHORTCUT.TOKEN_ERROR)
        if token_raw['uid'] == name and token_raw['password'] == password:
            access_id = token_raw['access_id']
    # endregion
    res = jh_user.login(name, password)
    shortcut = res['shortcut']
    if shortcut == SHORTCUT.OK:
        user = User.create_or_update(name, password, res['data']['email'])
    else:
        return tool.create_res_template(shortcut)
    act = UserActivity.create_or_update(user, 'index', device_type, get_ip(request), access_id)
    return JsonResponse(
        {'shortcut': SHORTCUT.OK,
         'msg': 'login success.',
         'data': act.to_dic(act.token)}
    )


def logout(request: HttpRequest):
    """
    登出账户
    :param request:
    :return:
    """
    # region params -> token
    args = tool.get_args(request)
    if args is None:
        return Http404()
    try:
        token = tool.check_token(args['token'])
    except KeyError:
        return tool.create_res_template(SHORTCUT.AE)
    except ValueError as e:
        return tool.create_res_afe(e.args[0])
    act = UserActivity.get(token)
    if act is None:
        return tool.create_res_template(SHORTCUT.TOKEN_ERROR)
    else:
        act.state = UserActivity.State.FAIL
        act.save()
        return JsonResponse(
            {'shortcut': SHORTCUT.OK,
             'msg': 'logout ok.'}
        )


def autologin(request: HttpRequest):
    """
    自动登录
    :param request:
    :return:
    """
    args = tool.get_args(request)
    if args is None:
        return Http404()
    try:
        token = tool.check_token(args['token'])
    except KeyError:
        return tool.create_res_template(SHORTCUT.AE)
    except ValueError as e:
        return tool.create_res_afe(e.args[0])
    act = UserActivity.get(token)
    if act is None:
        return tool.create_res_template(SHORTCUT.TOKEN_ERROR)

    return tool.fetch(token, extensions.get_ip(request), lambda x:
        {'msg': 'autologin ok',
         'shortcut': SHORTCUT.OK,
         'data': x.to_dic(x.token)}, True)


def getaccessinfo(request: HttpRequest):

    args = tool.get_args(request)
    if args is None:
        return Http404()
    try:
        token = tool.check_token(args['token'])
    except KeyError:
        return tool.create_res_template(SHORTCUT.AE)
    except ValueError as e:
        return tool.create_res_afe(e.args[0])
    return tool.fetch(token, extensions.get_ip(request), lambda x:
        {'msg': 'query ok',
         'shortcut': 'ok',
         'data': [item.to_dic_simple() for item in UserActivity.objects.filter(user=x.user)]}
    )



