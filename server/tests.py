
from django.utils import timezone
from django.conf import settings
from django.test import TestCase
from django.core.files import File
from django.contrib.auth.models import User, AnonymousUser

from rest_framework.test import APITestCase
from rest_framework import status

import os
import shutil
import subprocess
import time
import paramiko
import mock
from datetime import datetime

from .models import (
    Origin,
    BaseDestination,
    LocalDestination,
    SFTPDestination,
    APIDestination,
    Backup
)

from .views import (
    UserViewSet,
    DestinationViewSet,
    BackupViewSet
)


PATH=os.path.join(settings.BASE_DIR, 'examples')

def mock_sftp_connect(self):
    pkey = paramiko.RSAKey.from_private_key_file('test_rsa.key')
    transport = paramiko.Transport(('localhost', 3373))
    transport.connect(username='admin', password='admin', pkey=pkey)
    return paramiko.SFTPClient.from_transport(transport)

def create_sftp_server():
    return subprocess.Popen(['sftpserver', '-k', 'test_rsa.key', '-l', 'WARNING'])

def rm_dir_files(dirname):
    for fname in os.listdir(dirname):
        file_path = os.path.join(dirname, fname)
        try:
            if os.path.isfile(file_path) and 'reactive_course source code_reactive-week1.zip' not in file_path:
                print 'remove file %s' % file_path
                os.remove(file_path)
            elif os.path.isdir(file_path):
                print 'remove dir %s' % file_path
                rm_dir_files(file_path)
                shutil.rmtree(file_path)
        except Exception, e:
            print 'ERROR %s' % e
            pass
        
    
# Create your tests here.

class DestinationCase(TestCase):

    def setUp(self):
        o = Origin.objects.create(
            name = 'Guadalupe',
            plan = 'blablablablabla'
        )
        
        self.user = User.objects.create(
            username='Guadalupe',
            email='g@g.com'
        )
        
        ld1 = LocalDestination.objects.create(
            name = 'HD1',
            directory = os.path.join(PATH, 'destination1')
        )
        
        ld2 = LocalDestination.objects.create(
            name = 'HD2',
            directory = os.path.join(PATH, 'destination2')
        )
        
        sftp1 = SFTPDestination.objects.create(
            name = 'TestSFTPDestination',
            hostname = 'localhost',
            port = '3373',
            username = 'admin',
            key_filename = os.path.expanduser('test_rsa.key')
        )
        
        api1 = APIDestination.objects.create(
            name = 'Amazon S3',
            pubkey = r'TyByYXRvIHJvZXUgYSByb3VwYSBkbyByZWkgZGUgcm9tYQ',
            base_uri = r'https://aws.amazon.com/s3/',
            set_uri = r'/object/',
            get_uri  = r'/object/'
        )
        
        dt = timezone.now()
        fn = 'backup_%s.tar.gz' % dt.strftime(settings.DT_FORMAT)
        
        Backup.objects.create(
            user = self.user,
            #origin = o,
            name = fn,
            destination = ld2.basedestination_ptr,
            date = dt
        )
        
        Backup.objects.create(
            user = self.user,
            #origin = o,
            name = fn,
            destination = sftp1.basedestination_ptr,
            date = dt
        )
        
        self.fn = os.path.join(PATH, 'reactive_course source code_reactive-week1.zip')
    
    @classmethod
    def tearDownClass(cls):
        rm_dir_files('Guadalupe')
        rm_dir_files(PATH)
        
    def test_localbackup(self):
        
        #b = Backup.objects.get(origin__pk=1,
        #                       destination__name='HD2')
        b = Backup.objects.get(user__pk=self.user.id,
                               destination__name='HD2')
        
        #contents = File(self.fn).open('rb')
        contents = File(open(self.fn, 'rb'))
        b.backup(contents)
        
        self.assertTrue(b.success)
        self.assertFalse(b.before_restore)
        self.assertFalse(b.after_restore)
        self.assertIsNone(b.restore_dt)
        self.assertIsNone(b.related_to)
        
        #print (b,
        #       b.name,
        #       b.origin,
        #       b.destination,
        #       b.date,
        #       b.success,
        #       b.before_restore,
        #       b.after_restore,
        #       b.restore_dt,
        #       b.related_to)
        
    def test_localrestore(self):
        #b = Backup.objects.get(origin__pk=1,
        #                       destination__name='HD2')
        b = Backup.objects.get(user__pk=self.user.id,
                               destination__name='HD2')
        #print b.__dict__
        
        data = b.restore()
        
        self.assertIsNotNone(data)
        self.assertEquals(''.join(data), open(self.fn, 'rb').read())
        
        #if not data is None:
        #    print 'success'
        #    print len(data)
        #else:
        #    print 'fail'
    
    #@mock.patch.object(SFTPDestination, 'connect', side_effect='mock_sftp_connect')    
    def test_sftpbackup(self):
        proc = create_sftp_server()
        
        time.sleep(0.3)
        b = None
        with mock.patch.object(SFTPDestination, 'connect', return_value=mock_sftp_connect(None)) as mocked_func:
            #b = Backup.objects.get(origin__pk=1,
            #                       destination__name='TestSFTPDestination')
            b = Backup.objects.get(user__pk=self.user.id,
                                   destination__name='TestSFTPDestination')
            
            contents = File(open(self.fn, 'rb'))
            b.backup(contents)
        
        proc.kill()
        
        self.assertTrue(b.success)
        self.assertFalse(b.before_restore)
        self.assertFalse(b.after_restore)
        self.assertIsNone(b.restore_dt)
        self.assertIsNone(b.related_to)
        
        
    def test_sftprestore(self):
        proc = create_sftp_server()
        time.sleep(0.3)
        
        data = None
        with mock.patch.object(SFTPDestination, 'connect', return_value=mock_sftp_connect(None)) as mocked_func:
            #b = Backup.objects.get(origin__pk=1,
            #                   destination__name='TestSFTPDestination')
            b = Backup.objects.get(user__pk=self.user.id,
                               destination__name='TestSFTPDestination')
            data = b.restore()
        
        proc.kill()
        
        self.assertIsNotNone(data)
        self.assertEquals(''.join(data), open(self.fn, 'rb').read())

    
class APILoginTestCase(APITestCase):
    def setUp(self):
        users = [
            { 'username': 'admin', 'email': 'a@a.com', 'is_superuser': True },
            { 'username': 'default', 'email': 'd@d.com', 'is_superuser': False }
        ]
        for u_info in users:
            user = User.objects.create(username=u_info['username'], email=u_info['email'], is_superuser=u_info['is_superuser'])
            user.set_password(u_info['username'])
            user.save()
    
    def test_api_authenticate_username_password(self):
        user = User.objects.get(username='admin')
        logged_in = self.client.login(username=user.username, password=user.username)
        self.client.logout()
        
        self.assertTrue(logged_in)
    
    def test_api_authenticate_token(self):
        user = User.objects.get(username='admin')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + user.auth_token.key)
        response = self.client.get('/users/', format='json')
        self.client.logout()
        
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertNotIn('error', response.data)
    
    
    
class APIAdminTestCase(APITestCase):
    
    def setUp(self):
        users = [
            { 'username': 'admin', 'email': 'a@a.com', 'is_superuser': True },
            { 'username': 'default', 'email': 'd@d.com', 'is_superuser': False }
        ]
        for u_info in users:
            user = User.objects.create(username=u_info['username'], email=u_info['email'], is_superuser=u_info['is_superuser'])
            user.set_password(u_info['username'])
            user.save()
        user = User.objects.get(username='admin')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + user.auth_token.key)
    
    def tearDown(self):
        self.client.logout()
    
    def test_api_get_users_auth_admin(self):
        response = self.client.get('/users/', format='json')
        
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertNotIn('error', response.data)
    
    def test_api_get_user_auth_admin(self, ):
        response = self.client.get('/users/2/', format='json')
        
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertNotIn('error', response.data)
        