# -*- coding: utf-8 -*-

from tastypie.resources import ModelResource
from tastypie.authorization import Authorization, ReadOnlyAuthorization
from tastypie import fields
from tastypie.authentication import Authentication
#from tastypie.authentication import ApiKeyAuthentication
#from tastypie.authentication import authenticate
#from tastypie.authentication import BasicAuthentication 
#from tastypie.authentication import DigestAuthentication
#from tastypie.authentication import HttpUnauthorized
from server.models.Origin import Origin
from server.models.Backup import Backup
from server.models.destination.BaseDestination import BaseDestination
#from server.models.destination.APIDestination import APIDestination
#from server.models.destination.LocalDestination import LocalDestination
#from server.models.destination.SFTPDestination import SFTPDestination

class OriginResource(ModelResource):
    class Meta:
        queryset = Origin.objects.all()
        authorization = Authorization()
        resource_name = u'origin'
        excludes = ['id','date_created', 'date_modified',]
        allowed_methods = ['get','post', 'put', 'delete']
        
    
class DestinationResource(ModelResource):
    class Meta:
        queryset = BaseDestination.objects.all()
        resource_name = u'destination'
        authorization = ReadOnlyAuthorization()
        excludes = ['id', 'directory', 'date_created', 'date_modified',]
        list_allowed_methods = ['get']
        detail_allowed_methods = []
        
    
class BackupResource(ModelResource):
    origin      = fields.ForeignKey(OriginResource, 'origin')
    destination = fields.ForeignKey(DestinationResource, 'destination')
    
    class Meta:
        queryset = Backup.objects.all()
        resource_name = u'backup'
        authorization = Authorization()
        excludes = ['date_created', 'date_modified', 'id']
        allowed_methods = ['get', 'post']

class RecoverResource(ModelResource):
    class Meta:
        queryset = Backup.objects.all()
        resource_name = u'recover'
        authorization = ReadOnlyAuthorization()
        excludes = ['date_created', 'date_modified', 'id']
        allowed_methods = ['get']
    
