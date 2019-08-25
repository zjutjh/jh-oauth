from django.http import JsonResponse, HttpRequest
from .. import config
from ..models import User, UserActivity
from ..consts import SHORTCUT
from re import match
from ..apis import jh_user

ae = JsonResponse(
    {'msg': 'argument mismatch',
     'shortcut': 'ae'}, status=400)


def check_device_type(arg):
    if arg is None:
        return None
    if arg in ['mobile', 'pc', 'mobile_web', 'pc_web', 'pad']:
        return arg
    raise ValueError(f'device_type {arg} is not supported')


def check_normal(arg):
    if arg is None:
        return None
    if match(r'[a-zA-Z0-9_]{4,15}$', arg) is not None:
        return arg
    raise ValueError(f'{arg} is invalid')


def check_name(arg):
    if arg is None:
        return None
    if match(r'[a-zA-Z0-9_]{2,20}$', arg) is not None:
        return arg
    raise ValueError(f'{arg} is invalid for username')


def check_appname(arg):
    if arg is None:
        return None
    if match(r'[a-zA-Z0-9_]{2,20}$', arg) is not None:
        return arg
    raise ValueError(f'{arg} is invalid for appname')


def check_password(arg):
    if arg is None:
        return None
    if match(r'[a-zA-Z0-9_]{6,128}$', arg) is not None:
        return arg
    raise ValueError(f'{arg} is invalid for password')


def check_token(arg):
    if arg is None:
        return None
    return arg


def check_app_title(arg):
    if arg is None:
        return None
    if 1 <= len(arg) <= 128:
        return arg
    raise ValueError(f'{arg} is invalid for title')


def check_app_state(arg):
    if arg is None:
        return None
    if arg in ['wait', 'success', 'fail']:
        return arg
    raise ValueError(f'{arg} is invalid for state')


def create_res_template(shortcut, msg=None):
    if shortcut == SHORTCUT.AE:
        dic = {'shortcut': 'ae',
               'msg': 'argument mismatch'}
    elif shortcut == SHORTCUT.AFE:
        dic = {'shortcut': 'afe',
               'msg': 'argument format error.'}
    elif shortcut == SHORTCUT.PWE:
        dic = {'shortcut': 'pwe',
               'msg': 'password is error.'}
    elif shortcut == SHORTCUT.UNE:
        dic = {'shortcut': 'une',
               'msg': 'user is not existed.'}
    elif shortcut == SHORTCUT.TLE:
        dic = {'shortcut': 'tle',
               'msg': 'token is too old or user is logout.'}
    elif shortcut == SHORTCUT.SE:
        dic = {'shortcut': 'se',
               'msg': 'software not support this api.'}
    elif shortcut == SHORTCUT.TOKEN_ERROR:
        dic = {'shortcut': 'te',
               'msg': 'token is invalid.'}
    elif shortcut == SHORTCUT.PE:
        dic = {'shortcut': 'pe',
               'msg': 'you have no access to this.'}
    elif shortcut == SHORTCUT.ANE:
        dic = {'shortcut': 'ane',
               'msg': 'app not existed.'}
    elif shortcut == SHORTCUT.AKE:
        dic = {'shortcut': 'ake',
               'msg': 'appkey is invalid.'}
    elif shortcut == SHORTCUT.CE:
        dic = {'shortcut': 'ce',
               'msg': 'code is invalid'}
    else:
        raise ValueError('shortcut is invalid.')
    if msg is not None:
        dic['msg'] = msg
    return JsonResponse(dic)


def create_res_afe(msg):
    return JsonResponse(
        {'shortcut': SHORTCUT.AFE,
        'msg': msg}
    )


def get_args(request: HttpRequest):
    if request.method == 'GET' and config.MODE == 'debug':
        return request.GET
    elif request.method == 'POST':
        return request.POST
    else:
        return None


def fetch(token, ip, func, is_one_login=False):
    """
    通用的函数，用于用户操作时自动更新用户的状态。
    :param token:
    :param ip:
    :param func: 成功后的回调函数
    :param is_one_login: 是否只允许一个act处于活跃状态
    :return:
    """
    act = UserActivity.get(token)
    if act is None:
        return create_res_template(SHORTCUT.TOKEN_ERROR)
    if act.software == 'index':
        if act.alive:
            shortcut = act.user.check_password()
            if shortcut == SHORTCUT.OK:
                act.update(ip)
                if is_one_login:
                    UserActivity.assert_one_login(act)
                return JsonResponse(func(act))
            return create_res_template(shortcut)
        return create_res_template(SHORTCUT.TLE)
    return create_res_template(SHORTCUT.SE)

