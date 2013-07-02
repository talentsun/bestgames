from django.conf.urls import patterns, include, url

urlpatterns = patterns('analyse.views',
    url(r'^$', 'index'),
)
