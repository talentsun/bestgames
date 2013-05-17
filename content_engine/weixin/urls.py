from django.conf.urls import patterns, include, url

urlpatterns = patterns('weixin.views',
    url(r'^$', 'index'),
    url(r'^search/$', 'search'),
    url(r'^load/$', 'load'),
    url(r'^dialogs/add','add_edit_dialog'),
    url(r'^dialogs/(?P<dialog_id>\d+)/edit','add_edit_dialog'),
    url(r'^dialogs/(?P<dialog_id>\d+)/delete','delete_dialog'),
)
