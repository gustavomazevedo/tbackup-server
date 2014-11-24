# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Backup.file_upload'
        db.add_column(u'server_backup', 'file_upload',
                      self.gf('django.db.models.fields.files.FileField')(max_length=100, null=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Backup.file_upload'
        db.delete_column(u'server_backup', 'file_upload')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'server.apidestination': {
            'Meta': {'object_name': 'APIDestination', '_ormbases': ['server.BaseDestination']},
            'base_uri': ('django.db.models.fields.CharField', [], {'max_length': '1024'}),
            u'basedestination_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['server.BaseDestination']", 'unique': 'True', 'primary_key': 'True'}),
            'get_uri': ('django.db.models.fields.CharField', [], {'default': "'/get/'", 'max_length': '1024'}),
            'pubkey': ('django.db.models.fields.TextField', [], {}),
            'set_uri': ('django.db.models.fields.CharField', [], {'default': "'/set/'", 'max_length': '1024'})
        },
        'server.backup': {
            'Meta': {'object_name': 'Backup'},
            'after_restore': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'before_restore': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'date': ('django.db.models.fields.DateTimeField', [], {}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
            'destination': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['server.BaseDestination']"}),
            'file_upload': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '1024'}),
            'obs': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'related_to': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['server.Backup']", 'null': 'True', 'blank': 'True'}),
            'restore_dt': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'success': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
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