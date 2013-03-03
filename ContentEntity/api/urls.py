__author__ = 'huwei'

from django.conf.urls.defaults import *
from api.views import HotGamesViewFunc

urlpatterns = patterns('',
    url(r'^$',HotGamesViewFunc),
)