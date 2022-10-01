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
    url(r'^change-password/$', PasswordChange.as_view(), name='Password_Change'),

    ## Login History
    url(r'^login-history/$', LoginHistoryView, name='login_history'),
    url(r'^delete-history/$', DeleteHistory, name='delete_history'),
]