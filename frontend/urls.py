from django.conf.urls import url
from django.contrib import admin
from .views import *
from .sitemaps import *
from django.contrib.sitemaps.views import sitemap
from django.conf import settings
from django.conf.urls.static import static


admin.autodiscover()

app_name = 'frontend'

sitemaps = {
    'pages': StaticSitemap,
}

urlpatterns = [
    url(r'^$', index, name='index'),
    # url(r'^about-us/$', AboutUs, name='abouts'),
    # url(r'^privacy-policy/$', PrivacyPolicy, name='privacy_policy'),
    # url(r'^terms-and-conditions/$', TermsAndConditions, name='terms_and_conditions'),
    # url(r'^sitemap.xml/$', sitemap, {'sitemaps': sitemaps}),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
