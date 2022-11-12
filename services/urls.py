from django.conf.urls import url
from django.contrib import admin
from .views import *

admin.autodiscover()
app_name = 'services'

urlpatterns = [
    url(r'^services-list/$',ServicesListView, name='services_list'),
]