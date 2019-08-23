from django.http import HttpRequest, HttpResponse
from ..apis import jh_user
import json


def login(request: HttpRequest):
    username = request.GET['username']
    password = request.GET['password']
    response = jh_user.login(username, password)
    data = json.load(response)
    print(data)
    return HttpResponse('hello world')
