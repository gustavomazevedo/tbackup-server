#-*- coding: utf-8 -*-

from ..mixins import (
    NameableMixin,
    LoggableMixin
)


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
        app_label = 'server'
        