from django.urls import path
from . import views

urlpatterns = [
    path('oauth', views.oauth, name='test.oauth'),
    path('', views.create, name='test.create')
]