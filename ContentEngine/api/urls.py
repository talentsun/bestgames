__author__ = 'huwei'

from django.conf.urls.defaults import *

urlpatterns = patterns('api.views',
    url(r'^$','index'),
    url(r'^auth$','auth'),
    url(r'^login$','sina_login'),
    url(r'^rediers/add','add_rediers'),
    url(r'^games/add','add_edit_game'),
    url(r'^games/(?P<game_id>\d+)/edit','add_edit_game'),
    url(r'^games/(?P<game_id>\d+)/delete','delete_game'),
    url(r'^completed','completed'),
)