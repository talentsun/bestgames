from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
import settings

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'ContentEngine.views.home', name='home'),
    # url(r'^ContentEngine/', include('ContentEngine.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^static/(?P<path>.*)$','django.views.static.serve',{'document_root': settings.STATIC_ROOT}),
    url(r'^media/(?P<path>.*)$','django.views.static.serve',{'document_root': settings.MEDIA_ROOT}),
    url(r'^ajax-upload/', include('ajax_upload.urls')),
    url(r'^ext/', include('django_select2.urls')),
    url(r'', include('api.urls')),
    url(r'', include('social_auth.urls')),
    url(r'^weixin/', include('weixin.urls')),
)

urlpatterns += staticfiles_urlpatterns()


