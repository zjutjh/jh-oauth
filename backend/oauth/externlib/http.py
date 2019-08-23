import urllib
import urllib.request
import json


def get(base_url, **args):
    url = f"{base_url}?{'&'.join((f'{key}={value}' for key,value in args.items()))}"
    response = urllib.request.urlopen(url, data=None, timeout=10)
    return response


def post(base_url, **args):
    response = urllib.request.urlopen(base_url, data=args, timeout=10)


