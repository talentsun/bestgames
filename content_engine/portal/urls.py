__author__ = 'huwei'

from django.conf.urls.defaults import *

urlpatterns = patterns('portal.views',
    url(r'^$','index'),
    url(r'^rediers/add','add_edit_redier'),
    url(r'^rediers/(?P<redier_id>\d+)/edit','add_edit_redier'),
    url(r'^rediers/(?P<redier_id>\d+)/delete','delete_redier'),
    url(r'^games/add','add_edit_game'),
    url(r'^games/(?P<game_id>\d+)/preview','preview_game'),
    url(r'^games/(?P<game_id>\d+)/edit','add_edit_game'),
    url(r'^games/(?P<game_id>\d+)/delete','delete_game'),
    url(r'^collections/add','add_edit_collection'),
    url(r'^collections/(?P<collection_id>\d+)/edit','add_edit_collection'),
    url(r'^collections/(?P<collection_id>\d+)/delete','delete_collection'),
    url(r'^collections/(?P<collection_id>\d+)/preview','preview_collection'),
    url(r'^problems/add','add_edit_problem'),
    url(r'^problems/(?P<problem_id>\d+)/edit','add_edit_problem'),
    url(r'^problems/(?P<problem_id>\d+)/delete','delete_problem'),
    url(r'^weixinmsg/add','add_edit_weixin'),
    url(r'^weixinmsg/(?P<weixin_id>\d+)/edit','add_edit_weixin'),
    url(r'^weixinmsg/(?P<weixin_id>\d+)/delete','delete_weixin'),
    url(r'^player/add','add_edit_player'),
    url(r'^player/(?P<player_id>\d+)/edit','add_edit_player'),
    url(r'^player/(?P<player_id>\d+)/delete','delete_player'),
    url(r'^logout', 'logout')
)
