__author__ = 'huwei'

from django.conf.urls.defaults import *

urlpatterns = patterns('scrapy_itunes.views',
    url(r'^tools/url2icon','getPic'),
    url(r'^pic/(?P<filename>\w+\.jpg)','previewImage'),
)
