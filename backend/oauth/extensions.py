from .security import Aes
import hashlib
from django.utils import timezone
from django.http import HttpRequest
import pytz
from . import config
import binascii

aes = Aes(config.AES_KEY)


def get_md5(value: str):
    md5 = hashlib.md5()
    md5.update(value.encode('utf-8'))
    return md5.hexdigest()


def default_time():
    time = timezone.datetime(1970, 1, 1, 0, 0, 0, 0, pytz.timezone('UTC'))
    print(time)
    return time


def format_time(time: timezone.datetime):
    return time.astimezone().strftime('%Y-%m-%d %H:%M:%S')


def now():
    return timezone.datetime.now().astimezone()


def ticks(time: timezone.datetime):
    print(time)
    delta = time - default_time()
    return int(delta.total_seconds())


def get_ip(request: HttpRequest):
    try:
        return request.META['HTTP_X_FORWARDER_FOR']
    except KeyError:
        return request.META['REMOTE_ADDR']


def encrypt_token(uid: str, access_id: str, software: str, device_type: str):
    token_raw = f'{uid}::{software}::{access_id}::{device_type}'
    return aes.encrypt(token_raw)


def decrypt_token(token: str):
    """
    获取原有的登录信息
    :param token: 登录的token
    :return:
    """
    try:
        token_raw = aes.decrypt(token)
    except binascii.Error:
        return None
    args = token_raw.split('::')
    return {'uid': args[0], 'software': args[1],  'access_id': args[2], 'device_type': args[3]}


def encrypt_refresh_token(uid: str, access_id: str, software: str, device_type: str):
    token_raw = f'refresh::{uid}::{software}::{access_id}::{device_type}'
    return aes.encrypt(token_raw)


def decrypt_refresh_token(token: str):
    """
    获取原有的登录信息
    :param token: 登录的token
    :return:
    """
    try:
        token_raw = aes.decrypt(token)
    except binascii.Error:
        return None
    args = token_raw.split('::')
    return {'uid': args[1], 'software': args[2],  'access_id': args[3], 'device_type': args[4]}


def encrypt_code(name: str, appkey: str, access_id: str):
    token_raw = f'{name}::{appkey}::{access_id}'
    return aes.encrypt(token_raw)


def decrypt_code(token: str):
    token_raw = aes.decrypt(token)
    args = token_raw.split('::')
    return {'name': args[0], 'appkey': args[1], 'access_id': args[2]}
