# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Origin'
        db.create_table(u'server_origin', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=1024)),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('date_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, auto_now_add=True, blank=True)),
            ('plan', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('server', ['Origin'])

        # Adding model 'BaseDestination'
        db.create_table(u'server_basedestination', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=1024)),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('date_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, auto_now_add=True, blank=True)),
            ('directory', self.gf('django.db.models.fields.CharField')(default=u'~', max_length=1024, blank=True)),
        ))
        db.send_create_signal('server', ['BaseDestination'])

        # Adding model 'Backup'
        db.create_table(u'server_backup', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=1024)),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('date_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, auto_now_add=True, blank=True)),
            ('origin', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['server.Origin'])),
            ('destination', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['server.BaseDestination'])),
            ('date', self.gf('django.db.models.fields.DateTimeField')()),
            ('success', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('obs', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('restore_dt', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('before_restore', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('after_restore', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('related_to', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['server.Backup'], null=True, blank=True)),
        ))
        db.send_create_signal('server', ['Backup'])

        # Adding model 'LocalDestination'
        db.create_table(u'server_localdestination', (
            (u'basedestination_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['server.BaseDestination'], unique=True, primary_key=True)),
        ))
        db.send_create_signal('server', ['LocalDestination'])

        # Adding model 'SFTPDestination'
        db.create_table(u'server_sftpdestination', (
            (u'basedestination_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['server.BaseDestination'], unique=True, primary_key=True)),
            ('hostname', self.gf('django.db.models.fields.CharField')(max_length=1024)),
            ('port', self.gf('django.db.models.fields.CharField')(max_length=5, blank=True)),
            ('username', self.gf('django.db.models.fields.CharField')(default=u'tbackup', max_length=80)),
            ('key_filename', self.gf('django.db.models.fields.CharField')(max_length=80)),
        ))
        db.send_create_signal('server', ['SFTPDestination'])

        # Adding model 'APIDestination'
        db.create_table(u'server_apidestination', (
            (u'basedestination_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['server.BaseDestination'], unique=True, primary_key=True)),
            ('pubkey', self.gf('django.db.models.fields.TextField')()),
            ('base_uri', self.gf('django.db.models.fields.CharField')(max_length=1024)),
            ('set_uri', self.gf('django.db.models.fields.CharField')(default='/set/', max_length=1024)),
            ('get_uri', self.gf('django.db.models.fields.CharField')(default='/get/', max_length=1024)),
        ))
        db.send_create_signal('server', ['APIDestination'])


    def backwards(self, orm):
        # Deleting model 'Origin'
        db.delete_table(u'server_origin')

        # Deleting model 'BaseDestination'
        db.delete_table(u'server_basedestination')

        # Deleting model 'Backup'
        db.delete_table(u'server_backup')

        # Deleting model 'LocalDestination'
        db.delete_table(u'server_localdestination')

        # Deleting model 'SFTPDestination'
        db.delete_table(u'server_sftpdestination')

        # Deleting model 'APIDestination'
        db.delete_table(u'server_apidestination')


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
            'origin': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['server.Origin']"}),
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
        'server.origin': {
            'Meta': {'object_name': 'Origin'},
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