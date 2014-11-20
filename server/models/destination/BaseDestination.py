#-*- coding: utf-8 -*-
from django.db import models

from ..mixins import (
    NameableMixin,
    LoggableMixin
)

class BaseDestination(NameableMixin, LoggableMixin):
    
    directory = models.CharField(verbose_name=u'diretório',
                                 max_length=1024,
                                 blank=True,
                                 default=u'~')
    
    @property
    def destination_impl(self):
        return (self._getattr('localdestination',
                self._getattr('sftpdestination',
                self._getattr('apidestination',
                None))))
    
    @property
    def type(self):
        return self.destination_impl.__class__.__name__
    
    def backup(self, *args, **kwargs):
        return self.destination_impl.backup(*args,**kwargs)
    def restore(self, *args, **kwargs):
        return self.destination_impl.restore(*args,**kwargs)
    
    def _getattr(self, attr, otherwise):
        try:
            return getattr(self, attr, otherwise)
        except:
            return otherwise
    
    def get_or_create(self, *args, **kwargs):
        print '*args'
        print args
        print '**kwargs'
        print kwargs
        
        return super(BaseDestination, self).get_or_create(*args, **kwargs)
        #new_attrs = dict()
        #new_attrs['name'] = attrs['name']
        #
        #if instance:
        #    if instance.type == 'LocalDestination':
        #        new_attrs['directory'] = attrs['localdestination']['directory']
        #        return LocalDestination(**new_attrs)
        #    elif instance.type == 'SFTPDestination':
        #        new_attrs['directory'] = attrs['sftpdestination']['directory']
        #        new_attrs['hostname'] = attrs['sftpdestination']['hostname']
        #        new_attrs['port'] = attrs['sftpdestination']['port']
        #        new_attrs['username'] = attrs['sftpdestination']['username']
        #        new_attrs['key_filename'] = attrs['sftpdestination']['key_filename']
        #        return SFTPDestination(**new_attrs)
        #
        #new_attrs['directory'] = attrs['localdestination']['directory']
        #return LocalDestination(**new_attrs)

        
    class Meta:
        verbose_name = 'destino'
        app_label = 'server'
