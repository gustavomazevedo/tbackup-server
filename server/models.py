# -*- coding: utf-8 -*-
#language imports
from datetime import datetime
import os

#lib imports
from django.conf     import settings
from django.db       import models
#from tastypie.models import create_api_key

#own imports
from .mixins.model_mixins import (
    NameableMixin,
    LoggableMixin,
    AccessableMixin,
    APIMixin
    )


# Create your models here.
class Origin(NameableMixin, LoggableMixin):
    plan = models.TextField(verbose_name=u'plano')
    
    class Meta:
        verbose_name        = u'origem'
        verbose_name_plural = u'origens'

#hooking model creation to ApiKey generation
#models.signals.post_save(create_api_key, sender=Origin)
#

#class Server(NameableMixin, AccessableMixin, APIMixin, LoggableMixin):
#    
#    class Meta:
#        verbose_name = u'servidor'

class Destination(NameableMixin, LoggableMixin):
    @property
    def destination_impl(self):
        return self._getattr('localdestination',
               self._getattr('sftpdestination',
               self._getattr('apidestination',
               None)))
    
    def backup(self, *args, **kwargs):
        return self.destination_impl.backup(*args,**kwargs)
    def restore(self, *args, **kwargs):
        return self.destination_impl.restore(*args,**kwargs)
    
    def _getattr(self, attr, otherwise):
        try:
            return getattr(self, attr, otherwise)
        except:
            return otherwise
    
    class Meta:
        abstract = False
    
class LocalDestination(Destination):
    directory = models.CharField(verbose_name=u'diretório',
                                 max_length=1024,
                                 blank=True,
                                 default=u'~')
    
    def backup(self, contents, subdir, filename, *args, **kwargs):
        print "Hello! This is %s's backup method" % self.__class__.__name__
        fd = os.path.join(self.directory, subdir)
        if not os.path.exists(fd):
            os.makedirs(fd)
        fn = os.path.join(fd,filename)
        try:
            with open(fn, 'wb+') as f:
                for data in iter(lambda: contents.read(64 * 1024), ''):
                    f.write(data)
        except Exception, e:
            print e
            return False
        return True
        
    def restore(self, subdir, filename, *args, **kwargs):
        print "Hello! This is %s's restore method" % self.__class__.__name__
        fn = os.path.join(self.directory,
                          subdir,
                          filename)
        try:
            with open(fn, 'rb') as f:
                return ((data for data in iter(lambda: f.read(64 * 1024), '')), True)
        except Exception, e:
            print e
            return None, False
    
    
    class Meta:
        verbose_name = u'destino local'
        verbose_name_plural = u'destinos locais'

class SFTPDestination(Destination, AccessableMixin):
    
    def backup(self, *args, **kwargs):
        print "Hello! This is %s's backup method" % self.__class__.__name__
        #raise NotImplementedError
    def restore(self, filename):
        print "Hello! This is %s's restore method" % self.__class__.__name__
        #raise NotImplementedError
    
    class Meta:
        verbose_name = u'destino SFTP'
        verbose_name_plural = u'destinos SFTP'

class APIDestination(Destination, APIMixin):
    
    def backup(self, *args, **kwargs):
        print "Hello! This is %s's backup method" % self.__class__.__name__
        #raise NotImplementedError
    def restore(self, filename):
        #print "Hello! This is %s's restore method" % self.__class__.__name__
        raise NotImplementedError
    
    class Meta:
        verbose_name = u'destino API'
        verbose_name_plural = u'destinos API'

class Backup(NameableMixin, LoggableMixin):
    origin         = models.ForeignKey(Origin)
    destination    = models.ForeignKey(Destination)
    date           = models.DateTimeField(verbose_name=u'data do backup')
    success        = models.BooleanField(default=False)    
    obs            = models.TextField(null=True,
                                   blank=True)
    '''Restore data and consequences:
            (date,
            emergency backup before restore,
            dummy backup after restore,
            original backup related to this after/before restore)
    '''
    restore_dt     = models.DateTimeField(verbose_name=u'data do último restauro',
                                          blank=True,
                                          null=True)
    before_restore = models.BooleanField(default=False)
    after_restore  = models.BooleanField(default=False)
    related_to     = models.ForeignKey('Backup', null=True, blank=True)
    
    def backup(self, contents, before_restore=False, after_restore=False):
        #shortcut
        #if after_backup, just send obs message
        if after_restore:
            self.after_restore = True
            self.obs = u'Restauro da data %s bem sucedido!' % (
                self.related_to.restore_dt.strftime(settings.DT_FORMAT_VERBOSE))
            self.success = True
            self.save()
            return True
        
        success = self.destination.backup(
            subdir = self.origin.name,
            filename = self.name,
            contents = contents
        )
        if success:
            self.success = True
            if before_restore:
                self.before_restore = True
                self.obs = u'Backup de resguardo %s bem sucedido!' % (
                    self.related_to.restore_dt.strftime(settings.DT_FORMAT_VERBOSE))
            self.save()
        return success    
    
    def restore(self):
        contents, success = self.destination.restore(
            subdir = self.origin.name,
            filename = self.name
        )
        if success:
            self.restore_dt = datetime.now()
            self.obs = u'Tentativa de restauro na data %s' % (
                self.restore_dt.strftime(settings.DT_FORMAT_VERBOSE))
            self.save()
            return contents
        return None
        

#class Log(models.Model, LoggableMixin):
#    origin      = models.ForeignKey(Origin)
#    destination = models.ForeignKey(Destination)
#    date        = models.DateTimeField(verbose_name=u'data do backup')
#    filename    = models.CharField(verbose_name=u'nome do arquivo',
#                                   max_length=1024)
#    success     = models.BooleanField()
