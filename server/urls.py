from django.conf.urls import patterns, include, url

urlpatterns = patterns( 'server.views'
, url(r'^register_origin/$'         , 'register_origin')
, url(r'^(?P<id>\w+)/destinations/$', 'retrieve_destinations')
, url(r'^(?P<id>\w+)/backup/$'      , 'backup')
, url(r'^(?P<id>\w+)/restore/$'     , 'restore')
, url(r'^(?P<id>\w+)/message/$'     , 'message')
)
