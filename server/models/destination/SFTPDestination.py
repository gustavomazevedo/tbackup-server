#-*- coding: utf-8 -*-

import os
import errno
import logging
import paramiko

from django.db import models

from .BaseDestination import BaseDestination
from ..mixins     import AccessableMixin

class SFTPDestination(AccessableMixin, BaseDestination):
    
    client = None
    
    def connect(self):
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.client.load_system_host_keys()
        pvtkey = paramiko.RSAKey.from_private_key_file(os.path.expanduser(self.key_filename))
        
        self.client.connect(hostname=self.hostname,
                       port=int(self.port),
                       username=self.username,
                       pkey=pvtkey,
                       timeout=5.0)
        return self.client.open_sftp()
    
    def backup(self, contents, subdir, filename, *args, **kwargs):
        #print "Hello! This is %s's backup method" % self.__class__.__name__

        fd = os.path.join(self.directory, subdir)
        
        sftp = None
        
        try:
            sftp = self.connect()
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
            sftp.close()
            if self.client:
                self.client.close()
            return True
        except:
            if sftp:
                sftp.close()
            if self.client:
                self.client.close()
            raise

    
    def restore(self, subdir, filename, *args, **kwargs):
        #print "Hello! This is %s's restore method" % self.__class__.__name__
        
        try:
            sftp = self.connect()
            sftp.chdir(subdir)
                
            with sftp.open(filename, 'rb') as f:
                data = [chunks for chunks in iter(lambda: f.read(64 * 1024), '')]
                sftp.close()
                return (data, True)
        except Exception, e:
            print e
            logging.error(e, errno)
            sftp.close()
            return (None, False)
    
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