from django.conf.urls import patterns, include, url

urlpatterns = patterns('weixin.views',
    url(r'^$', 'index'),
    url(r'^search/$', 'search'),
    url(r'^load/$', 'load'),
    url(r'^gifts/(?P<user_id>\d+)', 'gifts'),
    url(r'^puzzles/(?P<puzzle_id>\d+)', 'puzzles'),
    url(r'^puzzles', 'puzzles'),
    url(r'^intro','intro')
)
