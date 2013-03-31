__author__ = 'huwei'

from django.conf.urls.defaults import *
import settings

urlpatterns = patterns('scrapy_itunes.views',
    url(r'^getPic','getPic'),
    url(r'^pic/(?P<filename>\.*)/edit','previewImage'),
)