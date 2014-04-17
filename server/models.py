# -*- coding: utf-8 -*-
from django.conf     import settings
from django.db       import models
from tastypie.models import create_api_key

from .mixins import (
    NameableMixin,
    AccessableMixin,
    APIMixin,
    LoggableMixin
    )

# Create your models here.
class Origin(NameableMixin, LoggableMixin):
    plan = models.TextField(verbose_name=u'plano')
    
    class Meta:
        verbose_name        = u'origem'
        verbose_name_plural = u'origens'

#hooking model creation to ApiKey generation
models.signals.post_save(create_api_key, sender=Origin)

class Server(NameableMixin, AccessableMixin, APIMixin, LoggableMixin):
    
    class Meta:
        verbose_name = u'servidor'

class Destination(NameableMixin, LoggableMixin):
    @property
    def destination_impl(self):
        return getattr(self, 'localdestination',
               getattr(self, 'sftpdestination',
               getattr(self, 'apidestination', None)))
    
    def backup(self, *args, **kwargs):
        return self.destination_impl.backup(*args,**kwargs)
    def restore(self, *args, **kwargs):
        return self.destination_impl.restore(*args,**kwargs)
    
class LocalDestination(Destination):
    directory = models.CharField(verbose_name=u'diretório',
                                 max_length=1024,
                                 blank=True,
                                 default=u'~')
    
    def backup(self, filename, *args, **kwargs):
        raise NotImplementedError
    def restore(self, filename):
        raise NotImplementedError
    
    class Meta:
        verbose_name = u'destino local'
        verbose_name_plural = u'destinos locais'

class SFTPDestination(Destination, AccessableMixin):
    
    def backup(self, *args, **kwargs):
        raise NotImplementedError
    def restore(self, *args, **kwargs):
        raise NotImplementedError
    
    class Meta:
        verbose_name = u'destino SFTP'
        verbose_name_plural = u'destinos SFTP'

class APIDestination(Destination, APIMixin):
    def backup(self, *args, **kwargs):
        raise NotImplementedError
    def restore(self, *args, **kwargs):
        raise NotImplementedError
    
    class Meta:
        verbose_name = u'destino API'
        verbose_name_plural = u'destinos API'


class Log(models.Model, LoggableMixin):
    origin      = models.ForeignKey(Origin)
    destination = models.ForeignKey(Destination)
    date        = models.DateTimeField(verbose_name=u'data do backup')
    filename    = models.CharField(verbose_name=u'nome do arquivo',
                                   max_length=1024)
    success     = models.BooleanField()