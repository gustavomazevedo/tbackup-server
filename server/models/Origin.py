#-*- coding: utf-8 -*-

import uuid
import hmac
try:
    from hashlib import sha1
except ImportError:
    import sha
    sha1 = sha.sha
    
from django.db import models

from .mixins import (
    NameableMixin,
    LoggableMixin
)

class Origin(NameableMixin, LoggableMixin, models.Model):
    plan   = models.TextField(verbose_name=u"plano")
    apikey = models.CharField(max_length=256)
    
    class Meta:
        verbose_name        = u"origem"
        verbose_name_plural = u"origens"
        app_label = u"server"
    
    def save(self, *args, **kwargs):
        if not self.apikey:
            self.apikey = hmac.new(
                uuid.uuid4().bytes,
                digestmod=sha1
            ).hexdigest()
        return super(Origin, self).save(*args, **kwargs)
    
    