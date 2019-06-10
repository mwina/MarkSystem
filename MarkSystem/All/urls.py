from django.conf import settings
from django.conf.urls import url
from django.views.static import serve

from All import views

urlpatterns = [
    url('login', views.login),
    url('index', views.index),
    url('checked', views.checked),
    url('show', views.show),
    url('list', views.list),
    url('gcore', views.gcore),
]
