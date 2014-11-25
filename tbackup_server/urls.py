from django.conf.urls import patterns, include, url
from django.views.generic import RedirectView

from django.contrib import admin
admin.autodiscover()

from rest_framework import routers
from server.views import UserViewSet, DestinationViewSet, BackupViewSet

# Routers provide a way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'destinations', DestinationViewSet)
router.register(r'backups', BackupViewSet)
#router.register(r'rrules', RRuleViewSet)

from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls), name='admin'),
    url(r'^server/', include('server.urls')),
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api-token-auth/', obtain_auth_token),
    #url(r'^docs/', include('rest_framework_swagger.urls')),
)
