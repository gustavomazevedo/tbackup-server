#-*- coding: utf-8 -*-

from .Destination import Destination
from ..mixins     import APIMixin

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
        app_label = 'server'