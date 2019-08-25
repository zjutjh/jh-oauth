from oauth.apis import http
from . import api
import json
from ..consts import RESPONSE, SHORTCUT
import logging


def _login(uid, password):
    return http.get(api.jh_user, app='passport', action='login', passport=uid, password=password)


def login(username, password):
    """
    向外界提供的接口，用于向精弘用户中心的服务器发送登录请求，返回格式为 dic{ shortcut, data }
    :param username:
    :param password:
    :return:
    """
    res = _login(username, password)
    if res.status == RESPONSE.OK:
        res_json = json.load(res)
        logging.debug(f'JH_USER LOGIN response json={res_json}')
        if res_json['state'] == 'success':
            data = res_json['data']
            return {
                'shortcut': SHORTCUT.OK,
                'data': {
                    'username': data['pid'],
                    'password': password,
                    'email': data['email']
                }
            }
        else:
            if '密码不正确' in res_json['info']:
                return {
                    'shortcut': SHORTCUT.PWE
                }
            else:
                return {
                    'shortcut': SHORTCUT.UNE
                }

