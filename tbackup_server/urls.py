from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from tastypie.api import Api
from server.api.v1.resources import (
    OriginResource,
    DestinationResource,
    BackupResource,
    RecoverResource
    )

v1_api = Api(api_name='v1')
v1_api.register(OriginResource())
v1_api.register(DestinationResource())
v1_api.register(BackupResource())
v1_api.register(RecoverResource())

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'tbackup_server.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^server/', include('server.urls')),
    url(r'^api/', include(v1_api.urls)),
)
