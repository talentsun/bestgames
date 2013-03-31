__author__ = 'huwei'

from django.conf.urls.defaults import *

urlpatterns = patterns('scrapy_itunes.views',
    url(r'^getPic','getPic'),
    url(r'^pic/(?P<filename>\w+\.jpg)','previewImage'),
)