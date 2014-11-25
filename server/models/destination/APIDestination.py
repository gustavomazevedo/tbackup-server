#-*- coding: utf-8 -*-

from .BaseDestination import BaseDestination
from ..mixins     import APIMixin

class APIDestination(APIMixin, BaseDestination):
    
    def backup(self, *args, **kwargs):
        print "Hello! This is %s's backup method" % self.__class__.__name__
        #raise NotImplementedError
    def restore(self, filename):
        #print "Hello! This is %s's restore method" % self.__class__.__name__
        raise NotImplementedError
    
    class Meta:
        verbose_name = u'destino API'
        verbose_name_plural = u'destinos API'
        app_label = 'server'