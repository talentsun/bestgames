__author__ = 'huwei'

from django.conf.urls.defaults import *
from api.views import index,auth,sina_login,add_rediers,add_games,completed

urlpatterns = patterns('',
    url(r'^$',index),
    url(r'^auth$',auth),
    url(r'^login$',sina_login),
    url(r'^rediers/add',add_rediers),
    url(r'^games/add',add_games),
    url(r'^completed',completed)
)