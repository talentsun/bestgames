from django.conf.urls import patterns, include, url

urlpatterns = patterns('weixin.views',
    url(r'^$', 'index'),
    url(r'^search/$', 'search'),
    url(r'^load/$', 'load'),
)
