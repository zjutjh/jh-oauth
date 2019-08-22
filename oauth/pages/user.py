from django.http import HttpRequest, HttpResponse, JsonResponse, Http404
import json

from oauth import extensions
from . import tool
from ..extensions import config, get_ip
from ..models import AppScheme, User, UserActivity
from ..apis import jh_user


def login(request: HttpRequest):
    """
    用户登录操作，可指定旧的token以保留access_id信息
    :param request:
    :return:
    """
    try:
        # region params -> name,password,device_type,[token]
        args = tool.get_args(request)
        if args is None:
            return Http404()
        name = args['name']
        password = args['password']
        device_type = args['device_type']
        try:
            token_raw = extensions.decrypt_token(args['token'])
            if token_raw['uid'] == name and token_raw['password'] == password:
                access_id = token_raw['access_id']
            else:
                access_id = None
        except KeyError:
            access_id = None
        # endregion
        # region 检查用户
        user = User.get(name)
        if user is None:
            text = jh_user.x_login(name, password)
            if text == 'pe':
                return JsonResponse(
                    {'msg': 'password error',
                     'shortcut': 'pe'}
                )
            elif text == 'une':
                return JsonResponse(
                    {'msg': 'user not existed',
                     'shortcut': 'une'}
                )
            user = User.get(name)
        # endregion
        if User.checkpw(name, password):
            ip = get_ip(request)
            act = UserActivity.x_update(user, 'index', device_type, ip, access_id)
            tool.push(act)
            return JsonResponse(
                {'msg': 'login ok',
                 'shortcut': 'ok',
                 'data': act.to_dic(act.token)}
            )
        else:
            return JsonResponse(
                {'msg': 'password error',
                 'shortcut': 'pe'}
            )

    except KeyError:
        return tool.ae
    except Exception as e:
        return tool.error(e)


def logout(request: HttpRequest):
    """
    登出账户
    :param request:
    :return:
    """
    try:
        # region params -> token
        args = tool.get_args(request)
        if args is None:
            return Http404()
        token = args['token']
        act = UserActivity.get(token)
        if act is None:
            return JsonResponse(
                {'msg': 'token is invalid.',
                 'shortcut': 'e'}
            )
        else:
            act.state = 'fail'
            act.save()
            return JsonResponse(
                {'msg': 'logout ok.',
                 'shortcut': 'ok'}
            )

    except KeyError:
        return tool.ae
    except Exception as e:
        return tool.error(e)


def autologin(request: HttpRequest):
    """
    自动登录
    :param request:
    :return:
    """
    try:
        args = tool.get_args(request)
        if args is None:
            return Http404()
        token = args['token']
        act = UserActivity.get(token)
        if act is None:
            return JsonResponse(
                {'msg': 'token is invalid.',
                 'shortcut': 'e'}
            )
        else:
            return tool.fetch(token, extensions.get_ip(request), lambda x:
                {'msg': 'autologin ok',
                 'shortcut': 'ok',
                 'data': x.to_dic(x.token)}, True)
    except KeyError:
        return tool.ae
    except Exception as e:
        return tool.error(e)


def getstate(request: HttpRequest):
    try:
        args = tool.get_args(request)
        if args is None:
            return Http404()
        token = args['token']
        return tool.fetch(token, extensions.get_ip(request), lambda x:
            {'msg': 'query ok',
             'shortcut': 'ok',
             'data': x.to_dic_state()}
        )
    except KeyError:
        return tool.ae
    except Exception as e:
        return tool.error(e)


def getaccessinfo(request: HttpRequest):
    try:
        args = tool.get_args(request)
        if args is None:
            return Http404()
        token = args['token']
        return tool.fetch(token, extensions.get_ip(request), lambda x:
            {'msg': 'query ok',
             'shortcut': 'ok',
             'data': [item.to_dic_simple() for item in UserActivity.objects.filter(user=x.user)]}
        )
    except KeyError:
        return tool.ae
    except Exception as e:
        return tool.error(e)

