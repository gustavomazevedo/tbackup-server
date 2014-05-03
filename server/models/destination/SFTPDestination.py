#-*- coding: utf-8 -*-


import errno

import paramiko

from .Destination import Destination
from ..mixins     import AccessableMixin

class SFTPDestination(Destination, AccessableMixin):
    
    def backup(self, contents, subdir, filename, *args, **kwargs):
        print "Hello! This is %s's backup method" % self.__class__.__name__
        client = paramiko.SSHClient()
        client.load_system_host_keys()
        client.connect(hostname=self.hostname,
                       port=self.port,
                       username=self.username,
                       password=self.password,
                       timeout=5.0)
        sftp = paramiko.SFTPClient.from_transport(client.get_transport())
        
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
    
    def restore(self, filename):
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
    
    def _rexists(sftp, path):
        try:
            sftp.stat(path)
        except IOError, e:
            if e.errno == errno.ENOENT:
                print e, errno
                return False
            else:
                pass
            raise
        else:
            return True
        
    class Meta:
        verbose_name = u'destino SFTP'
        verbose_name_plural = u'destinos SFTP'
        app_label = 'server'