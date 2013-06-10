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
    url(r'^weixinmsgs/add','add_edit_weixin'),
    url(r'^weixinmsgs/(?P<weixin_id>\d+)/edit','add_edit_weixin'),
    url(r'^weixinmsgs/(?P<weixin_id>\d+)/delete','delete_weixin'),
    url(r'^weixinmsgs/(?P<weixin_id>\d+)/preview','preview_weixin'),
    url(r'^players/add','add_edit_player'),
    url(r'^players/(?P<player_id>\d+)/edit','add_edit_player'),
    url(r'^players/(?P<player_id>\d+)/delete','delete_player'),
    url(r'^players/(?P<player_id>\d+)/preview','preview_player'),
    url(r'^news/(?P<news_id>\d+)/delete','delete_news'),
    url(r'^news/add','add_edit_news'),
    url(r'^news/(?P<news_id>\d+)/edit','add_edit_news'),
    url(r'^news/(?P<news_id>\d+)/preview','preview_news'),
    url(r'^puzzles/(?P<puzzle_id>\d+)/delete','delete_puzzle'),
    url(r'^puzzles/add','add_edit_puzzle'),
    url(r'^puzzles/(?P<puzzle_id>\d+)/edit','add_edit_puzzle'),
    url(r'^logout', 'logout')
)
