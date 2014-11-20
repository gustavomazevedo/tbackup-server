#-*- coding: utf-8 -*-

import os
import errno
import logging
import paramiko

from django.db import models

from .BaseDestination import BaseDestination
from ..mixins     import AccessableMixin

class SFTPDestination(BaseDestination, AccessableMixin):
    
    def connect(self):
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.load_system_host_keys()
        pvtkey = paramiko.RSAKey.from_private_key_file(self.key_filename)
        
        client.connect(hostname=self.hostname,
                       port=int(self.port),
                       username=self.username,
                       pkey=pvtkey,
                       timeout=5.0)
        return client
    
    def backup(self, contents, subdir, filename, *args, **kwargs):
        print "Hello! This is %s's backup method" % self.__class__.__name__

        fd = os.path.join(self.directory, subdir)
        client = self.connect()
        
        try: 
            sftp = client.open_sftp()
            
            if not self._rexists(sftp,subdir):
                sftp.mkdir(subdir)
                logging.warning('caminho criado')
            
            sftp.chdir(subdir)
            try:
                with sftp.open(filename, 'wb+') as f:
                    for data in contents.chunks():
                        f.write(data)
            except Exception, e:
                print e
                logging.error(e, errno)
                raise
            return True
        except:
            sftp.close()
            client.close()
            raise

    
    def restore(self, subdir, filename, *args, **kwargs):
        print "Hello! This is %s's restore method" % self.__class__.__name__
        
        client = self.connect()

        try:
            sftp = client.open_sftp()
            sftp.chdir(subdir)
                
            with sftp.open(filename, 'rb') as f:
                return ([chunks for chunks in iter(lambda: f.read(64 * 1024), '')], True)
        except Exception, e:
            print e
            logging.error(e, errno)
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