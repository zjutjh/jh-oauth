from django.http import JsonResponse, HttpRequest
from .. import config
from ..models import User, UserActivity

ae = JsonResponse(
    {'msg': 'argument mismatch',
     'shortcut': 'ae'}, status=400)


def error(e: Exception):
    if config.MODE != 'debug':
        return JsonResponse(
            {'msg': 'other errors',
             'shortcut': 'oe',
             'data': str(e)}, status=400
        )
    else:
        raise e


def get_args(request: HttpRequest):
    if request.method == 'GET' and config.MODE == 'debug':
        return request.GET
    elif request.method == 'POST':
        return request.POST
    else:
        return None


def fetch(token, ip, func, ispush=False):
    act = UserActivity.get(token)
    if act.software == 'index':
        if act.alive:
            act.update(ip)
            if ispush:
                push(act)
            return JsonResponse(func(act))
        return JsonResponse(
            {'msg': 'token is too old or user is logout.',
             'shortcut': 'le'}
        )
    return JsonResponse(
        {
            'msg': f'app {act.software} is not the authority one, which is banned from normal autologin, please use oauth2.0 instead.',
            'shortcut': 'b'}
    )


def push(act: UserActivity):
    if act.software == 'index':
        # ADD 清除其他访问的状态,如果不需要可以直接删除
        act_other = UserActivity.objects.filter(user=act.user, software='index', device_type=act.device_type)
        for item in act_other:
            if item.access_id != act.access_id:
                item.p_state = 'fail'
            else:
                item.p_state = 'success'
            item.save()

