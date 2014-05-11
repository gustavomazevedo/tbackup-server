# -*- coding: utf-8 -*-

from tastypie.resources import ModelResource
from server.models.Origin import Origin
from server.models.Backup import Backup
from server.models.destination.BaseDestination import BaseDestination
from server.models.destination.APIDestination import APIDestination
from server.models.destination.LocalDestination import LocalDestination
from server.models.destination.SFTPDestination import SFTPDestination

class OriginResource(ModelResource):
    class Meta:
        queryset = Origin.objects.all()
        resource_name = u'origin'
        allowed_methods = ['get','post', 'put', 'delete']
        
    
class DestinationResource(ModelResource):
    class Meta:
        queryset = BaseDestination.objects.all()
        resource_name = u'destination'
        allowed_methods = ['get', 'post', 'put', 'delete']
    
class BackupResource(ModelResource):
    class Meta:
        queryset = Backup.objects.all()
        resource_name = u'backup'
        allowed_methods = ['get', 'post']

class RecoverResource(ModelResource):
    class Meta:
        queryset = Backup.objects.all()
        resource_name = u'recover'
        allowed_methods = ['get']
    
