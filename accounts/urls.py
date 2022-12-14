from django.conf.urls import url
from django.contrib import admin
from .views import *

admin.autodiscover()

app_name = 'accounts'

urlpatterns = [
    ## Admin
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^logout/$', LogOutView.as_view(), name='logout'),
    url(r'^edit-user/(?P<id>[-\w]+)/$', EditUser, name='edit_user'),
    url(r'^view/(?P<id>[-\w]+)/$',ViewUser, name='view_user'),
    url(r'^change-status-active/(?P<id>[-\w]+)/$',ChangeStatusActive, name='change_status_active'),
    url(r'^change-status-inactive/(?P<id>[-\w]+)/$',ChangeStatusInActive, name='change_status_inactive'),
    url(r'^change-status-delete/(?P<id>[-\w]+)/$',ChangeStatusDelete, name='change_status_delete'),
    url(r'^change-password/$', PasswordChange.as_view(), name='Password_Change'),
    url(r'^user-graph/$', UserGraph, name='user_graph'),

    ## Login History
    url(r'^login-history/$', LoginHistoryView, name='login_history'),
    url(r'^delete-history/$', DeleteHistory, name='delete_history'),

    ## Cities
    url(r'^cities-list/$', CitiesList, name='cities_list'),
    
    ## Users
    url(r'^customers-list/$', CustomersList, name='customers_list'),
    url(r'^service-providers-list/$', ServiceProvidersList, name='service_providers_list'),

]