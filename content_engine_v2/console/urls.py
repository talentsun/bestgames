from django.conf.urls.defaults import *

urlpatterns = patterns('console.views',
    url(r'^$','index'),
    url(r'^entities/add','add_edit_entity'),
    url(r'^entities/(?P<entity_id>\d+)/edit','add_edit_entity'),
    url(r'^entities/(?P<entity_id>\d+)/delete','delete_entity'),
    url(r'^logout', 'logout')
)