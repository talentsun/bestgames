__author__ = 'huwei'

from django.conf.urls.defaults import *
from api.views import HotGamesViewFunc,Auth,Sinalogin,report

urlpatterns = patterns('',
    url(r'^$',HotGamesViewFunc),
    url(r'^auth$',Auth),
    url(r'^login$',Sinalogin),
    url(r'^hotgame',report)
)