from django.test import TestCase
from .models import (
    Origin,
    Destination,
    LocalDestination,
    SFTPDestination,
    APIDestination,
    Backup
)
from datetime import datetime
from django.utils.timezone import utc
from django.conf import settings

import os

PATH='/Users/gustavo/'
#PATH='/home/gustavo.azevedo/Projects/'

# Create your tests here.

class DestinationCase(TestCase):

    def setUp(self):
        Origin.objects.create(
            name = 'Guadalupe',
            plan = 'blablablablabla'
        )
        
        LocalDestination.objects.create(
            name = 'HD1',
            directory = os.path.join(PATH, 'tbackup-server', 'tests-1')
        )
        
        LocalDestination.objects.create(
            name = 'HD2',
            directory = os.path.join(PATH, 'tbackup-server', 'tests')
        )
        
        SFTPDestination.objects.create(
            name = 'Gruyere',
            address = 'gruyere.lps.ufrj.br',
            port = '22',
            ssh_username = 'tbackup',
            ssh_password = '123456'
        )
        
        APIDestination.objects.create(
            name = 'Amazon S3',
            pubkey = r'TyByYXRvIHJvZXUgYSByb3VwYSBkbyByZWkgZGUgcm9tYQ',
            base_uri = r'https://aws.amazon.com/s3/',
            set_uri = r'/object/',
            get_uri  = r'/object/'
        )
        
    def backup(self):
        origin = Origin.objects.get(pk=1)
        destination = Destination.objects.get(name='HD2')
        
        dt = datetime.utcnow().replace(tzinfo=utc)
        fn = 'backup_%s.tar.gz' % dt.strftime(settings.DT_FORMAT)
        
        b = Backup.objects.create(
            origin = origin,
            name = fn,
            destination = destination,
            date = dt
        )
        fn2 = os.path.join(PATH, 'virtualenv-1.11.4.tar.gz')
        contents = open(fn2, 'rb')
        
        b.backup(contents)
        
        return b, fn, origin, destination, dt
        
    def test_backup(self):
        
        b, fn, origin, destination, dt = self.backup()
        
        self.assertEqual(b.name, fn)
        self.assertEqual(b.origin, origin)
        self.assertEqual(b.destination, destination)
        self.assertEqual(b.date, dt)
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
        
    def test_restore(self):
        b = self.backup()[0]
        
        bs = Backup.objects.all()
        b = bs[0]
        print b.__dict__
        
        #b = Backup.objects.get(pk=1)
        
        data = b.restore()
        
        self.assertIsNotNone(data)
        
        if not data is None:
            print 'success'
            print data
        else:
            print 'fail'
        
        
