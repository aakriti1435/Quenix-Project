from django.contrib import admin
from django.urls import path,include
from django.conf.urls import include, url
from django.conf import settings
from accounts.views import  AdminLoginView
from django.conf.urls.static import static
from django.views.static import serve

urlpatterns = [
    url(r'^admin/login/', AdminLoginView.as_view()),
    path('admin/', admin.site.urls),
    path('', include('frontend.urls')),
    path('accounts/', include('accounts.urls', 'accounts')),
    url('^accounts/', include('django.contrib.auth.urls')),
    path('backup/', include('backup.urls') , name="Back_up"),
    url(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}), 
    url(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}), 
] 

if settings.DEBUG is False:
    urlpatterns += static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

handler404 = 'frontend.views.handler404'
handler500 = 'frontend.views.handler500'
handler403 = 'frontend.views.handler403'
handler400 = 'frontend.views.handler400'