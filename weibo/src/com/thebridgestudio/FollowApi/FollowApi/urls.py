from django.conf.urls import patterns, include, url
import settings

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'FollowApi.views.home', name='home'),
    # url(r'^FollowApi/', include('FollowApi.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
    url(r'^static/(?P<path>.*)$','django.views.static.serve',{'document_root': settings.STATIC_ROOT}),
    url(r'^$', 'Competitors.views.index'),
    url(r'^add$', 'Competitors.views.add'),
    url(r'^follow$', 'Operations.views.Follow'),
    url(r'^finish_follow$', 'Operations.views.FinishFollow'),
    url(r'^follower_status$', 'Statistic.views.follower_status'),
    url(r'^get_pie_data$', 'Statistic.views.get_pie_data'),
)

urlpatterns += staticfiles_urlpatterns()
