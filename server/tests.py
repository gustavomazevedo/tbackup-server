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

# Create your tests here.

class DestinationCase(TestCase):

    def setUp(self):
        Origin.objects.create(
            name = 'Guadalupe',
            plan = 'blablablablabla'
        )
        
        LocalDestination.objects.create(
            name = 'HD1',
            directory = '/Users/gustavo/tbackup-server/tests-1/'
        )
        
        LocalDestination.objects.create(
            name = 'HD2',
            directory = '/Users/gustavo/tbackup-server/tests/'
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
        contents = open('/Users/gustavo/Downloads/ScalaByExample.pdf', 'rb')
        
        b.backup(contents)
        
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
        
        
