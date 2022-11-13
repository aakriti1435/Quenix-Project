from django.conf.urls import url
from django.contrib import admin
from .views import *

admin.autodiscover()
app_name = 'services'

urlpatterns = [
    url(r'^services-list/$',ServicesListView, name='services_list'),
    url(r'^add-service/$',AddServiceView, name='add_service'),
    url(r'^view-service/(?P<id>[-\w]+)/$',ViewService, name='view_service'),
    url(r'^delete-service/(?P<id>[-\w]+)/$',DeleteService, name='delete_service'),
]