#-*- coding: utf-8 -*-

from django.db import models

from .mixins import (
    NameableMixin,
    LoggableMixin
)

class Origin(NameableMixin, LoggableMixin):
    plan = models.TextField(verbose_name=u'plano')
    
    class Meta:
        verbose_name        = u'origem'
        verbose_name_plural = u'origens'
        app_label = 'server'