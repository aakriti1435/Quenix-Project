from django.contrib import admin
from .views import *
from django.urls import path
from django.conf.urls import include, url

admin.autodiscover()
app_name = 'api'

urlpatterns = [
    url(r'^cities-list/$', CitiesListView.as_view(), name='cities_list'),
    url(r'^generate-otp/$', GenerateOTP.as_view(), name='generate_otp'),
    url(r'^verify-otp/$', VerifyOTP.as_view(), name='verify_otp'),
    url(r'^check-user/$', CheckUser.as_view(), name='check_user'),
    url(r'^logout/$', LogOutView.as_view(), name='logout_view'),
]