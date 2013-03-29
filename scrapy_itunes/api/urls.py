__author__ = 'huwei'

from django.conf.urls.defaults import *

urlpatterns = patterns('api.views',
    url(r'^getPic','getPic'),
)