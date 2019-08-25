import urllib
import urllib.request
from ..consts import REQUEST, RESPONSE


def get(base_url, **args):
    """
    发送GET请求
    :param base_url:前缀url后，最终url由代码自动完成拼接
    :param args: 参数
    :return:
    """
    url = f"{base_url}?{'&'.join((f'{key}={value}' for key,value in args.items()))}"
    response = urllib.request.urlopen(url, data=None, timeout=REQUEST.TIMEOUT)
    return response


def post(base_url, **args):
    response = urllib.request.urlopen(base_url, data=args, timeout=REQUEST.TIMEOUT)


