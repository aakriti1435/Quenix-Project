from django.contrib import admin
from .views import *
from django.urls import path
from django.conf.urls import include, url

admin.autodiscover()
app_name = 'api'

urlpatterns = [
    url(r'^cities-list/$', CitiesListView.as_view(), name='cities_list'),
]