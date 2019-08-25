from django.http import HttpRequest, HttpResponse, Http404, JsonResponse
from . import tool

from ..extensions import config, get_ip
from ..models import AppScheme, User, UserActivity
from django.utils.timezone import datetime
from ..consts import SHORTCUT


def register(request: HttpRequest):
    """
    注册一个应用，并将其置于wait(等待激活)状态
    :param request:
    :return:
    """
    # region params -> token, appname,
    args = tool.get_args(request)
    if args is None:
        return Http404()
    try:
        token = tool.check_token(args['token'])
        appname = tool.check_appname(args['appname'])
        title = tool.check_app_title(args['title'])
        description = args['description']
    except KeyError:
        return tool.create_res_template(SHORTCUT.AE)
    except ValueError as e:
        return tool.create_res_afe(e.args[0])

    def create_app(act: UserActivity):
        app = AppScheme.create(act.user, appname, title, description)
        if app is None:
            return {'msg': 'app is existed',
                    'shortcut': SHORTCUT.PE}
        else:
            return {'msg': 'create app ok.',
                 'shortcut': SHORTCUT.OK,
                 'data': app.to_dic()}

    return tool.fetch(token, get_ip(request), lambda x: create_app(x))


def getcode(request: HttpRequest):
    """
    用户登录后使用，以获取code
    :param request:
    :return:
    """
    args = tool.get_args(request)
    if args is None:
        return Http404()
    try:
        token = tool.check_token(args['token'])
        appname = tool.check_appname(args['appname'])
    except KeyError:
        return tool.create_res_template(SHORTCUT.AE)
    except ValueError as e:
        return tool.create_res_afe(e.args[0])

    def _get_code(act: UserActivity):
        app = AppScheme.get(appname)
        if app is None:
            return {'msg': 'app not existed',
                    'shortcut': SHORTCUT.ANE}
        act_app = UserActivity.create_or_update(act.user, appname, act.device_type, act.access_ip, act.access_id)
        act_app.generate_code(app.appkey)
        act_app.save()
        return {'msg': 'get code ok',
             'shortcut': SHORTCUT.OK,
             'data': act_app.code}

    return tool.fetch(token, get_ip(request), lambda x: _get_code(x))


def create(request: HttpRequest):

    args = tool.get_args(request)
    if args is None:
        return Http404()
    try:
        code = tool.check_token(args['code'])
        appkey = tool.check_token(args['appkey'])
    except KeyError:
        return tool.create_res_template(SHORTCUT.AE)
    except ValueError as e:
        return tool.create_res_afe(e.args[0])
    try:
        act_app = UserActivity.code_effect(code, appkey)
    except KeyError:
        return tool.create_res_template(SHORTCUT.AFE)
    except ValueError:
        return tool.create_res_template(SHORTCUT.AKE)
    if act_app is None:
        return tool.create_res_template(SHORTCUT.CE)
    app = AppScheme.from_code(code)
    if app.state == AppScheme.State.SUCCESS:
        return JsonResponse({
            'msg': 'open oauth success',
            'shortcut': 'ok',
            'data': act_app.to_dic_oauth(act_app.token, act_app.refresh_token)
        })
    return tool.create_res_template(SHORTCUT.SE)


def login(request: HttpRequest):
    """
    使用第三方的token进行登录，并检查是否过期
    :param request:
    :return:
    """
    args = tool.get_args(request)
    if args is None:
        return Http404()
    try:
        token = tool.check_token(args['token'])
        appname = tool.check_appname(args['appname'])
    except KeyError:
        return tool.create_res_template(SHORTCUT.AE)
    except ValueError as e:
        return tool.create_res_afe(e.args[0])
    act = UserActivity.get(token)
    if act.alive and act.software == appname:
        act.update(get_ip(request))
        act_index = UserActivity.get_index_of(token)
        return tool.fetch(act_index.token, get_ip(request), lambda x:
            {'msg': f'login app {act.software} ok.',
             'shortcut': SHORTCUT.OK,
             'data': act.to_dic(act.token)})
    return tool.create_res_template(SHORTCUT.TLE)


def refresh(request: HttpRequest):
    """
    使用第三方的token进行登录，并检查是否过期
    :param request:
    :return:
    """
    args = tool.get_args(request)
    if args is None:
        return Http404()
    try:
        refresh_token = tool.check_token(args['refresh_token'])
        appname = tool.check_appname(args['appname'])
    except KeyError:
        return tool.create_res_template(SHORTCUT.AE)
    except ValueError as e:
        return tool.create_res_afe(e.args[0])
    act = UserActivity.from_refresh_token(refresh_token)
    if act is None:
        return tool.create_res_template(SHORTCUT.TOKEN_ERROR)
    if act.alive and act.software == appname:
        act.update(get_ip(request))
        act_index = UserActivity.get_index_of(act.token)
        return tool.fetch(act_index.token, get_ip(request), lambda x:
            {'msg': f'login app {act.software} ok.',
             'shortcut': SHORTCUT.OK,
             'data': act.to_dic(act.token)})
    return tool.create_res_template(SHORTCUT.TLE)


def getinfo(request: HttpRequest):
    """
    获取应用的基础信息
    :param request:
    :return:
    """

    args = tool.get_args(request)
    if args is None:
        return Http404()
    try:
        appname = tool.check_appname(args['appname'])
    except KeyError:
        return tool.create_res_template(SHORTCUT.AE)
    except ValueError as e:
        return tool.create_res_afe(e.args[0])
    app = AppScheme.get(appname)
    if app is None:
        return tool.create_res_template(SHORTCUT.ANE)
    return JsonResponse(
        {'msg': f'query ok',
         'shortcut': SHORTCUT.OK,
         'data': app.to_dic()}
    )


def move(request: HttpRequest):
    """
    TODO 转移应用的持有者
    :param request:
    :return:
    """
    pass


def changeapp(request: HttpRequest):
    """
    修改应用，只有管理员才能使用。
    :param request:
    :return:
    """
    args = tool.get_args(request)
    if args is None:
        return Http404()
    try:
        token = tool.check_token(args['token'])
        appname = tool.check_appname(args['appname'])
        title = tool.check_app_title(args.get('title', None))
        description = args.get('description', None)
        state = tool.check_app_state(args.get('state', None))
    except KeyError:
        return tool.create_res_template(SHORTCUT.AE)
    except ValueError as e:
        return tool.create_res_afe(e.args[0])

    def change_app(act: UserActivity):
        app = AppScheme.get(appname)
        if act.user.permission > User.Permission.NORMAL:
            if app is None:
                return tool.create_res_template(SHORTCUT.ANE)
            if title is not None:
                app.title = title
            if description is not None:
                app.description = description
            if state is not None:
                app.p_state = state
            app.save()
            return {
                'shortcut': SHORTCUT.OK,
                'msg': 'change app ok',
                'data': app.to_dic()
            }
        else:
            return tool.create_res_template(SHORTCUT.PE)

    return tool.fetch(token, get_ip(request), lambda x: change_app(x))
