#-*- coding: utf-8 -*-

from datetime import datetime

from django.db import models
from django.conf import settings
from django.utils import timezone

from .Origin import Origin
from .destination.BaseDestination import BaseDestination

from .mixins import (
    NameableMixin,
    LoggableMixin
)

class Backup(NameableMixin, LoggableMixin):
    origin         = models.ForeignKey(Origin)
    destination    = models.ForeignKey(BaseDestination)
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
    
    class Meta:
        app_label = 'server'
        #unique_together = ('name', 'origin', 'destination', 'date')
    
    
    def backup(self, contents, before_restore=False, after_restore=False):
        #shortcut
        #if after_backup, just send obs message
        print after_restore
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
            self.restore_dt = timezone.now()
            self.obs = u'Tentativa de restauro na data %s' % (
                self.restore_dt.strftime(settings.DT_FORMAT_VERBOSE))
            self.save()
            return contents
        return None