from django.http import HttpRequest, HttpResponse, Http404, JsonResponse
from . import tool
from ..extensions import config, get_ip
from ..models import AppScheme, User, UserActivity
from django.utils.timezone import datetime


def create(request: HttpRequest):
    """
    注册一个应用，并将其置于wait(等待激活)状态
    :param request:
    :return:
    """
    try:
        # region params -> token, appname,
        args = tool.get_args(request)
        if args is None:
            return Http404()
        token = args['token']
        appname = args['appname']
        try:
            title = args['title']
        except KeyError:
            title = None
        try:
            description = args['description']
        except KeyError:
            description = None

        def create_app(act: UserActivity):
            app = AppScheme.get(appname)
            if app is None:
                app = AppScheme(owner=act.user, name=appname, create_time=datetime.now())
                app.generate_appkey()
            if app.owner == act.user:
                if title is not None:
                    app.title = title
                if description is not None:
                    app.description = description
                app.save()
                return {
                    'msg': 'create_app ok',
                    'shortcut': 'ok',
                    'data': app.to_dic()
                }
            else:
                return {
                    'msg': f'app {title} is not yours.',
                    'shortcut': 'pe',
                }

        return tool.fetch(token, get_ip(request), lambda x: create_app(x))
    except KeyError:
        return tool.ae
    except Exception as e:
        return tool.error(e)


def getcode(request: HttpRequest):
    """
    返回临时的访问代码

    :param request:
    :return:
    """
    try:
        # region param -> appname,appkey
        args = tool.get_args(request)
        if args is None:
            return Http404()
        appname = args['appname']
        appkey = args['appkey']
        app = AppScheme.get(appname)
        if app is None:
            return JsonResponse(
                {'msg': f'app {appname} is not existed.',
                 'shortcut': 'ne'}
            )
        elif app.appkey != appkey:
            return JsonResponse(
                {'msg': 'appkey is not invalid.',
                 'shortcut': 'ke'}
            )
        elif app.p_state != 'success':
            return JsonResponse(
                {'msg': f'app {appname} has not access to oauth.',
                 'shortcut': 'pe'}
            )
        return JsonResponse(
            {'msg': 'getcode ok.',
             'shortcut': 'ok',
             'data': app.code}
        )
    except KeyError:
        return tool.ae
    except Exception as e:
        return tool.error(e)


def alive(request: HttpRequest):
    try:
        args = tool.get_args(request)
        if args is None:
            return Http404()
        code = args['code']
        try:
            state = AppScheme.alive(code)
            if state:
                app = AppScheme.from_code(code)
                if app.p_state == 'success':
                    return JsonResponse(
                        {'msg': 'code is alive',
                         'shortcut': 'ok',
                         'data': app.to_dic()}
                    )
                else:
                    return JsonResponse(
                        {'msg': f'app {app.name} has no access to oauth.',
                         'shortcut': 'pe'}
                    )
            else:
                return JsonResponse(
                    {'msg': 'code is not alive',
                     'shortcut': 'na'}
                )
        except KeyError:
            return JsonResponse(
                {'msg': 'code is invalid',
                 'shortcut': 'e'}
            )
    except KeyError:
        return tool.ae
    except Exception as e:
        return tool.error(e)


def openoauth(request: HttpRequest):
    try:
        args = tool.get_args(request)
        if args is None:
            return Http404()
        token = args['token']  # 这个是用户登录的token
        code = args['code']
        try:
            if AppScheme.allow_login(code):
                app = AppScheme.from_code(code)
                if app.p_state == 'success':
                    def open_app(act: UserActivity):
                        act_app = UserActivity.x_update(act.user, app.name, act.device_type, act.access_ip, act.access_id)
                        return {
                            'msg': 'open oauth success',
                            'shortcut': 'ok',
                            'data': act_app.to_dic()
                        }

                    return tool.fetch(token, get_ip(request), lambda x: open_app(x))
                else:
                    return JsonResponse(
                        {'msg': f'app {app.name} has no access to oauth.',
                         'shortcut': 'pe'}
                    )
            else:
                return JsonResponse(
                    {'msg': 'code is too old.',
                     'shortcut': 'le'}
                )
        except KeyError:
            return JsonResponse(
                {'msg': 'code is invalid.',
                 'shortcut': 'e'}
            )

    except KeyError:
        return tool.ae
    except Exception as e:
        return tool.error(e)


def login(request: HttpRequest):
    """
    使用第三方的token进行登录，并检查是否过期
    :param request:
    :return:
    """
    try:
        args = tool.get_args(request)
        if args is None:
            return Http404()
        token = args['token']
        software = args['software']
        appkey = args['appkey']
        act = UserActivity.get(token)
        app = AppScheme.get(software)
        if act is None or software != act.software or app is None or app.appkey != appkey or app.p_state != 'success':
            return HttpResponse(
                {'msg': 'code or appkey is invalid.',
                 'shortcut': 'e'}
            )
        else:
            if act.alive:
                act.update(get_ip(request))
                return JsonResponse(
                    {'msg': f'login app {act.software} ok.',
                     'shortcut': 'ok',
                     'data': act.to_dic()}
                )
            else:
                return JsonResponse(
                    {'msg': f'login app {act.software} failed, the token is too old.',
                     'shortcut': 'le'}
                )
    except KeyError:
        return tool.ae
    except Exception as e:
        return tool.error(e)


def getinfo(request: HttpRequest):
    """
    获取应用的基础信息
    :param request:
    :return:
    """
    try:
        args = tool.get_args(request)
        if args is None:
            return Http404()
        appname = args['appname']
        app = AppScheme.get(appname)
        if app is None:
            return JsonResponse(
                {'msg': f'app {appname} is not existed',
                 'shortcut': 'e'}
            )
        return JsonResponse(
            {'msg': f'query ok',
             'shortcut': 'ok',
             'data': app.to_dic()}
        )
    except KeyError:
        return tool.ae
    except Exception as e:
        return tool.error(e)


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
    try:
        args = tool.get_args(request)
        token = args['token']
        appname = args['appname']
        try:
            title = args['title']
        except KeyError:
            title = None
        try:
            description = args['description']
        except KeyError:
            description = None
        try:
            state = args['state']
        except KeyError:
            state = None

        def change_app(act: UserActivity):

            app = AppScheme.get(appname)
            if act.user.permission > 0:
                if app is None:
                    app = AppScheme(owner=act.user, name=appname, create_time=datetime.now())
                    app.generate_appkey()
                    if title is not None:
                        app.title = title
                    if description is not None:
                        app.description = description
                    if state is not None:
                        app.p_state = state
                    app.save()
                    return {
                        'msg': 'create_app ok',
                        'shortcut': 'ok',
                        'data': app.to_dic()
                    }
                return {
                    'msg': f'app {app.name} is not existed',
                    'shortcut': 'ne'
                }
            else:
                return {
                    'msg': f'only admin have access to change info',
                    'shortcut': 'pe'
                }

        return tool.fetch(token, get_ip(request), lambda x: change_app(x))

    except KeyError:
        return tool.ae
    except Exception as e:
        return tool.error(e)
