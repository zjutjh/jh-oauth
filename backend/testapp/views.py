from django.shortcuts import render
from django.http import HttpRequest, Http404

url_base = 'http://127.0.0.1/'


# Create your views here.
def oauth(request: HttpRequest):
    try:
        # if request.method == 'GET':
        #     code = request.GET['code']
        #     redirect = request.GET['redirect']
        # else:
        #     return Http404()
        return render(request, 'testapp/oauth.html')
    except KeyError:
        return Http404()


def create(request: HttpRequest):
    try:
        return render(request, 'testapp/create.html')
    except KeyError:
        return Http404()