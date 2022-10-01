from django.contrib.sitemaps import Sitemap
from django.urls import reverse

class StaticSitemap(Sitemap):
    changefreq = 'daily'
    priority = '0.5'

    def items(self):
        return [
            'frontend:abouts'
        ]

    def location(self, item):
        return reverse(item)
