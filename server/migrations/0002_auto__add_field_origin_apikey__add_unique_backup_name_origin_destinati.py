# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Origin.apikey'
        db.add_column(u'server_origin', 'apikey',
                      self.gf('django.db.models.fields.CharField')(default=u'', max_length=256),
                      keep_default=False)

        # Adding unique constraint on 'Backup', fields ['name', 'origin', 'destination', 'date']
        #db.create_unique(u'server_backup', ['name', 'origin_id', 'destination_id', 'date'])


    def backwards(self, orm):
        # Removing unique constraint on 'Backup', fields ['name', 'origin', 'destination', 'date']
        #db.delete_unique(u'server_backup', ['name', 'origin_id', 'destination_id', 'date'])

        # Deleting field 'Origin.apikey'
        db.delete_column(u'server_origin', 'apikey')


    models = {
        'server.apidestination': {
            'Meta': {'object_name': 'APIDestination', '_ormbases': ['server.BaseDestination']},
            'base_uri': ('django.db.models.fields.CharField', [], {'max_length': '1024'}),
            u'basedestination_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['server.BaseDestination']", 'unique': 'True', 'primary_key': 'True'}),
            'get_uri': ('django.db.models.fields.CharField', [], {'default': "'/get/'", 'max_length': '1024'}),
            'pubkey': ('django.db.models.fields.TextField', [], {}),
            'set_uri': ('django.db.models.fields.CharField', [], {'default': "'/set/'", 'max_length': '1024'})
        },
        'server.backup': {
            #'Meta': {'unique_together': "(('name', 'origin', 'destination', 'date'),)", 'object_name': 'Backup'},
						'Meta': {'object_name': 'Backup'},
            'after_restore': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'before_restore': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'date': ('django.db.models.fields.DateTimeField', [], {}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
            'destination': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['server.BaseDestination']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '1024'}),
            'obs': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'origin': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['server.Origin']"}),
            'related_to': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['server.Backup']", 'null': 'True', 'blank': 'True'}),
            'restore_dt': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'success': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'server.basedestination': {
            'Meta': {'object_name': 'BaseDestination'},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
            'directory': ('django.db.models.fields.CharField', [], {'default': "u'~'", 'max_length': '1024', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '1024'})
        },
        'server.localdestination': {
            'Meta': {'object_name': 'LocalDestination', '_ormbases': ['server.BaseDestination']},
            u'basedestination_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['server.BaseDestination']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'server.origin': {
            'Meta': {'object_name': 'Origin'},
            'apikey': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '1024'}),
            'plan': ('django.db.models.fields.TextField', [], {})
        },
        'server.sftpdestination': {
            'Meta': {'object_name': 'SFTPDestination', '_ormbases': ['server.BaseDestination']},
            u'basedestination_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['server.BaseDestination']", 'unique': 'True', 'primary_key': 'True'}),
            'hostname': ('django.db.models.fields.CharField', [], {'max_length': '1024'}),
            'key_filename': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'port': ('django.db.models.fields.CharField', [], {'max_length': '5', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'default': "u'tbackup'", 'max_length': '80'})
        }
    }

    complete_apps = ['server']