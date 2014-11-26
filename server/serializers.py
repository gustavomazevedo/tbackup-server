from rest_framework import serializers, fields
from rest_framework.authtoken.serializers import AuthTokenSerializer

from django.contrib.auth.models import User, AnonymousUser
from server.models import ( Backup
                          , BaseDestination
                          , LocalDestination
                          , SFTPDestination
                          )

# Serializers define the API representation.
class UserSerializer(serializers.HyperlinkedModelSerializer):
    auth_token = serializers.Field(source='auth_token')
    
    class Meta:
        model = User
        fields = ('id', 'url', 'username', 'auth_token', 'password', 'email', 'is_staff', 'is_superuser')
        read_only_fields = ('is_superuser',)
        write_only_fields = ('password',)
        
    def get_fields(self, *args, **kwargs):
        fields = super(UserSerializer, self).get_fields(*args, **kwargs)
        request = self.context.get('request', None)
        
        if not request or not request.user.is_staff:
            fields['is_staff'].read_only = True
            
        return fields
    
    def restore_object(self, attrs, instance=None):
        user = None
        if instance is not None:
            user = instance    
            user.email = attrs.get('email', user.email)
            if user.is_staff or user.is_superuser:
                user.is_staff = attrs.get('is_staff', user.is_staff)

        else:
            user = User(**attrs)
            
        password = attrs.get('password', None)
        if password is not None:
            user.set_password(password)
        
        return user
    
class LocalDestinationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = LocalDestination
        fields = ('directory',)

class SFTPDestinationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = SFTPDestination
        fields = ('directory', 'hostname', 'port', 'username', 'key_filename')

class DestinationSerializer(serializers.HyperlinkedModelSerializer):
    type = fields.CharField(max_length=30)
    localdestination = LocalDestinationSerializer(required=False)
    sftpdestination = SFTPDestinationSerializer(required=False)
    
    class Meta:
        model = BaseDestination
        fields = ('id', 'url', 'name', 'type', 'localdestination'
                 , 'sftpdestination', 'date_created', 'date_modified'
                 )
        read_only_fields = ('date_created', 'date_modified')
        
    def get_fields(self, *args, **kwargs):
        fields = super(DestinationSerializer, self).get_fields(*args, **kwargs)
        request = self.context.get('request', None)
        
        #if not admin
        if not request or not request.user.is_staff:
            #remove these fields
            for field in ( 'type'
                         , 'localdestination'
                         , 'sftpdestination'
                         , 'date_created'
                         , 'date_modified'):
                fields.pop(field)
        return fields
    
    def validate(self, attrs):
        return super(DestinationSerializer, self).validate(attrs)
    
    def restore_object(self, attrs, instance=None):
        new_attrs = dict()
        new_attrs['name'] = attrs['name']
        
        if instance:
            instance.name = attrs.get('name', instance.name)
            
            if instance.type == 'LocalDestination':
                localdestination = attrs.get('localdestination')
                instance.directory = localdestination.directory if localdestination.directory else instance.localdestination.directory
                
            elif instance.type == 'SFTPDestination':
                sftpdestination = attrs.get('sftpdestination')
                instance.directory = sftpdestination.directory if sftpdestination.directory else instance.sftpdestination.directory
                instance.hostname = sftpdestination.hostname if sftpdestination.hostname else instance.sftpdestination.hostname
                instance.port = sftpdestination.port if sftpdestination.port else instance.sftpdestination.port
                instance.username = sftpdestination.username if sftpdestination.username else instance.sftpdestination.username
                instance.key_filename = sftpdestination.key_filename if sftpdestination.key_filename else instance.sftpdestination.key_filename
                
            return instance
            
        if attrs['type'] == 'LocalDestination':
            new_attrs['directory'] = attrs['localdestination'].directory
            return LocalDestination(**new_attrs)
        elif attrs['type'] == 'SFTPDestination':
            new_attrs['directory'] = attrs['sftpdestination'].directory
            new_attrs['hostname'] = attrs['sftpdestination'].hostname
            new_attrs['port'] = attrs['sftpdestination'].port
            new_attrs['username'] = attrs['sftpdestination'].username
            new_attrs['key_filename'] = attrs['sftpdestination'].key_filename
            return SFTPDestination(**new_attrs)
        else:
            raise Exception('destination type is not implemented')    

class BackupSerializer(serializers.HyperlinkedModelSerializer):
    destination = serializers.SlugRelatedField(slug_field='name')
    
    class Meta:
        model = Backup
        fields = ('id', 'url', 'name', 'file', 'destination', 'date')
    
    #overrides user attribute with current logged in user
    def restore_object(self, attrs, instance=None):
        attrs[u'user'] = self.context.get('request').user
        return Backup(**attrs)
    