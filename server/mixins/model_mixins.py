# -*- coding: utf-8 -*-

from django.db import models

class NameableMixin(models.Model):
    name = models.CharField(verbose_name=u'nome',
                            max_length=80)
    def __unicode__(self):
        return self.name
    class Meta:
        abstract = True
        ordering = ['name']

class AccessableMixin(models.Model):
    address      = models.CharField(verbose_name=u'endereço',
                                    max_length=1024)
    port         = models.CharField(verbose_name=u'porta',
                                    max_length=5,
                                    blank=True)
    ssh_username = models.CharField(verbose_name=u'username SSH',
                                    max_length=80,
                                    default=u'tbackup')
    ssh_password = models.CharField(verbose_name=u'senha de acesso SSH',
                                    max_length=80)
    class Meta:
        abstract = True
    
class APIMixin(models.Model):
    pubkey   = models.TextField(verbose_name=u'chave pública')
    base_uri = models.CharField(verbose_name=u'URI base',
                                max_length=1024)
    set_uri  = models.CharField(verbose_name=u'URI de escrita',
                                max_length=1024,
                                default=r'/set/')
    get_uri  = models.CharField(verbose_name=u'URI de leitura',
                                max_length=1024,
                                default=r'/get/')
    class Meta:
        abstract = True

class LoggableMixin(models.Model):
    date_created  = models.DateTimeField(verbose_name=u'data de criação',
                                         auto_now_add=True)
    date_modified = models.DateTimeField(verbose_name=u'data de modificação',
                                         auto_now_add=True,
                                         auto_now=True)
    
    class Meta:
        abstract = True
    