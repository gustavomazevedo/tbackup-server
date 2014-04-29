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
from django.conf import settings

import os

#PATH='/Users/gustavo/'
PATH='/home/gustavo.azevedo/Projects/'

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
        
        
        
    def test_backup(self):
        
        origin = Origin.objects.get(pk=1)
        destination = Destination.objects.get(name='HD2')
        
        dt = datetime.now()
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
        
        assert b.name == fn
        assert b.origin == origin
        assert b.destination == destination
        assert b.date == dt
        assert b.success == True
        assert b.before_restore == False
        assert b.after_restore == False
        assert b.restore_dt is None
        assert b.related_to is None
        
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
        self.test_backup()
        
        bs = Backup.objects.all()
        b = bs[0]
        print b.__dict__
        
        #b = Backup.objects.get(pk=1)
        
        data = b.restore()
        
        assert not data is None
        
        if not data is None:
            print 'success'
            print data
        else:
            print 'fail'
        
        
