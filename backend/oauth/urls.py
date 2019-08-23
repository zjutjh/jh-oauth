from django.urls import path
from .pages import test, user, oauth

urlpatterns = [
    path('test/login', test.login, name='test.login'),
    path('api/user/login', user.login, name='user.login'),
    path('api/user/logout', user.logout, name='user.logout'),
    path('api/user/autologin', user.autologin, name='user.autologin'),
    path('api/user/getstate', user.getstate, name='user.getstate'),
    path('api/user/getaccessinfo', user.getaccessinfo, name='user.getaccessinfo'),
    path('api/oauth/create', oauth.create, name='oauth.create'),
    path('api/oauth/getcode', oauth.getcode, name='oauth.getcode'),
    path('api/oauth/alive', oauth.alive, name='oauth.alive'),
    path('api/oauth/openoauth', oauth.openoauth, name='oauth.openoauth'),
    path('api/oauth/getinfo', oauth.getinfo, name='oauth.getinfo'),
    path('api/oauth/move', oauth.move, name='oauth.move'),
    path('api/oauth/changeapp', oauth.changeapp, name='oauth.changeapp')
]
