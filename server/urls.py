from django.conf.urls import patterns, url

urlpatterns = \
    patterns( 'server.views'
            , url(r'^origin_available/$'        , 'origin_available')
            , url(r'^register_origin/$'         , 'register_origin')
            , url(r'^(?P<id>\d+)/destinations/$', 'retrieve_destinations')
            , url(r'^(?P<id>\d+)/backup/$'      , 'backup')
            , url(r'^(?P<id>\d+)/restore/$'     , 'restore')
            , url(r'^(?P<id>\d+)/message/$'     , 'message')
            )
