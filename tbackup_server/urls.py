from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from server.api.api import v1_api

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'tbackup_server.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^server/', include('server.urls')),
    url(r'^api/', include(v1_api.urls)),
)
