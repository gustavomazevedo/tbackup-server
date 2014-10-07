from django.test import TestCase
from .models import (
    Origin,
    BaseDestination,
    LocalDestination,
    SFTPDestination,
    APIDestination,
    Backup
)
from datetime import datetime
from django.utils import timezone
from django.conf import settings

from django.core.files import File

import os

PATH=os.path.join(settings.BASE_DIR, 'examples')
#PATH='/home/gustavo.azevedo/Projects/'

# Create your tests here.

class DestinationCase(TestCase):

    def setUp(self):
        o = Origin.objects.create(
            name = 'Guadalupe',
            plan = 'blablablablabla'
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
            name = 'TinyCore',
            hostname = '192.168.56.102',
            port = '22',
            username = 'gustavo',
            key_filename = os.path.expanduser('~/.ssh/testkey_rsa')
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
            origin = o,
            name = fn,
            destination = ld2.basedestination_ptr,
            date = dt
        )
        
        Backup.objects.create(
            origin = o,
            name = fn,
            destination = sftp1.basedestination_ptr,
            date = dt
        )
        
        self.fn = os.path.join(PATH, 'reactive_course source code_reactive-week1.zip')
        
    def test_localbackup(self):
        
        b = Backup.objects.get(origin__pk=1,
                               destination__name='HD2')
        
        #contents = File(self.fn).open('rb')
        contents = File(open(self.fn, 'rb'))
        b.backup(contents)
        
        self.assertTrue(b.success)
        self.assertFalse(b.before_restore)
        self.assertFalse(b.after_restore)
        self.assertIsNone(b.restore_dt)
        self.assertIsNone(b.related_to)
        
        print (b,
               b.name,
               b.origin,
               b.destination,
               b.date,
               b.success,
               b.before_restore,
               b.after_restore,
               b.restore_dt,
               b.related_to)
        
    def test_localrestore(self):
        b = Backup.objects.get(origin__pk=1,
                               destination__name='HD2')
        print b.__dict__
        
        data = b.restore()
        
        self.assertIsNotNone(data)
        
        if not data is None:
            print 'success'
            print data
        else:
            print 'fail'
        
    def test_sftpbackup(self):
        b = Backup.objects.get(origin__pk=1,
                               destination__name='TinyCore')
        
        contents = File(open(self.fn, 'rb'))
        b.backup(contents)
        
        self.assertTrue(b.success)
        self.assertFalse(b.before_restore)
        self.assertFalse(b.after_restore)
        self.assertIsNone(b.restore_dt)
        self.assertIsNone(b.related_to)
        
        print (b,
               b.name,
               b.origin,
               b.destination,
               b.date,
               b.success,
               b.before_restore,
               b.after_restore,
               b.restore_dt,
               b.related_to)
