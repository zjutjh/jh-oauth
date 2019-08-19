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
        try:
            tags = args['tags']
        except KeyError:
            tags = None
        try:
            level = args['level']
        except KeyError:
            level = None

        def create_app(act: UserActivity):
            app = AppScheme.get(appname)
            if app is None:
                app = AppScheme(owner=act.user, name=appname, create_time=datetime.now())
                app.generate_appkey()
            if title is not None:
                app.title = title
            if description is not None:
                app.description = description
            if tags is not None:
                app.tags = tags
            if level is not None:
                app.p_level = level
            app.save()
            return {
                'msg': 'create_app',
                'shortcut': 'ok',
                'data': app.to_dic()
            }

        return tool.fetch(token, get_ip(request), lambda x: create_app(x))

    except KeyError:
        return tool.ae


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
        return JsonResponse(
            {'msg': 'getcode ok.',
             'shortcut': 'ok',
             'data': app.code}
        )
    except KeyError:
        return tool.ae


def alive(request: HttpRequest):
    try:
        args = tool.get_args(request)
        if args is None:
            return Http404()
        code = args['code']
        try:
            # TODO 加入权限验证模块
            state = AppScheme.alive(code)
            if state:
                app = AppScheme.from_code(code)
                return JsonResponse(
                    {'msg': 'code is alive',
                     'shortcut': 'ok',
                     'data': app.to_dic()}
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


def openoauth(request: HttpRequest):
    try:
        args = tool.get_args(request)
        if args is None:
            return Http404()
        token = args['token']
        code = args['code']
        try:
            if AppScheme.allow_login(code):
                app = AppScheme.from_code(code)

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


def updateper(request: HttpRequest):
    """
    TODO 用于注册应用使用的权限，若当前不存在该权限，则自动创建
    :param request:
    :return:
    """
    pass


def getinfo(request: HttpRequest):
    """
    TODO 查看应用基础信息，包括权限的验证
    :param request:
    :return:
    """
    pass


def checkper(request: HttpRequest):
    """
    TODO 查看应用是否具有某项权限
    :param request:
    :return:
    """
    pass


def move(request: HttpRequest):
    """
    TODO 转移应用的持有者
    :param request:
    :return:
    """
    pass


def changeapp(request: HttpRequest):
    """
    TODO 修改应用的状态，包含基础的状态以及state
    :param request:
    :return:
    """
    pass
