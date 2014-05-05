#-*- coding: utf-8 -*-

import os
import errno
import logging
import paramiko

from django.db import models

from .BaseDestination import BaseDestination
from ..mixins     import AccessableMixin

class SFTPDestination(BaseDestination, AccessableMixin):
    
    def backup(self, contents, subdir, filename, *args, **kwargs):
        print "Hello! This is %s's backup method" % self.__class__.__name__

        fd = os.path.join(self.directory, subdir)
        
        #transport = paramiko.Transport((self.hostname, self.port))
        #transport.connect(username=self.username,
        #                  pkey=paramiko.RSAKey.from_private_key(rsa_private_key))
        #sftp = paramiko.SFTPClient.from_transport(transport)
        #
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.load_system_host_keys()
        print (self.hostname,
               int(self.port),
               self.username,
               )
        client.connect(hostname=self.hostname,port=int(self.port),username=self.username,timeout=5.0)
        try: 
            sftp = client.open_sftp()
            
            if not self._rexists(sftp,subdir):
                sftp.mkdir(subdir)
                logging.warning('caminho criado')
            
            sftp.chdir(subdir)
            #fn = os.path.join(fd, filename)
            fn = filename
            try:
                with sftp.open(fn, 'wb+') as f:
                    for data in contents.chunks():
                        f.write(data)
            except Exception, e:
                print e
                logging.error(e, errno)
                raise
            return True
        except:
            client.close()
            raise
    
    def restore(self, contents, subdir, filename, *args, **kwargs):
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
    
    def _rexists(self, sftp, path):
        """
            Verifica se arquivo existe no servidor remoto
            http://docs.python.org/2/library/errno.html#errno.ENOENT
        """
        try:
            sftp.stat(path)
        except IOError, e:
            if e.errno == errno.ENOENT:
                print e, errno
                return False
            raise
        else:
            return True
        
    class Meta:
        verbose_name = u'destino SFTP'
        verbose_name_plural = u'destinos SFTP'
        app_label = 'server'