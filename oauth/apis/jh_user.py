from ..externlib import http
from . import api
import json
from ..models import User


def login(uid, password):
    return http.get(api.jh_user, app='passport', action='login', passport=uid, password=password)


def x_login(uid, password):
    # 当发现没有存在该用户时，应该向上级转发登录请求
    response = login(uid, password)
    if response.status == 200:
        data = json.load(response)
        print(f'h={data}')
        if data['state'] == 'success':
            User.create_stu(uid, password, data['data']['email'])
            return 'ok'
        else:
            if '密码不正确' in data['info']:
                return 'pe'
            else:
                return 'une'