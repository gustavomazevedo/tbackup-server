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
from django.utils.timezone import utc
from django.conf import settings

from django.core.files import File

import os

PATH='/Users/gustavo/'
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
            directory = os.path.join(PATH, 'tbackup-server', 'tests-1')
        )
        
        ld2 = LocalDestination.objects.create(
            name = 'HD2',
            directory = os.path.join(PATH, 'tbackup-server', 'tests')
        )
        
        sftp1 = SFTPDestination.objects.create(
            name = 'Odin',
            hostname = '177.17.192.100',
            port = '22',
            username = 'testing'
        )
        
        api1 = APIDestination.objects.create(
            name = 'Amazon S3',
            pubkey = r'TyByYXRvIHJvZXUgYSByb3VwYSBkbyByZWkgZGUgcm9tYQ',
            base_uri = r'https://aws.amazon.com/s3/',
            set_uri = r'/object/',
            get_uri  = r'/object/'
        )
        
        dt = datetime.utcnow().replace(tzinfo=utc)
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
        
    def test_localbackup(self):
        
        b = Backup.objects.get(origin__pk=1,
                               destination__name='HD2')
        
        fn2 = os.path.join(PATH, 'virtualenv-1.11.4.tar.gz')
        contents = File(fn2).open('rb')
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
                               destination__name='Odin')
        
        fn2 = os.path.join(PATH, 'virtualenv-1.11.4.tar.gz')
        contents = File(open(fn2, 'rb'))
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
