# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Course.faculty'
        db.alter_column(u'nerdeez_server_app_course', 'faculty_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['nerdeez_server_app.Faculty']))

        # Changing field 'Faculty.university'
        db.alter_column(u'nerdeez_server_app_faculty', 'university_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['nerdeez_server_app.University']))

    def backwards(self, orm):

        # Changing field 'Course.faculty'
        db.alter_column(u'nerdeez_server_app_course', 'faculty_id', self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['nerdeez_server_app.Faculty']))

        # Changing field 'Faculty.university'
        db.alter_column(u'nerdeez_server_app_faculty', 'university_id', self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['nerdeez_server_app.University']))

    models = {
        u'nerdeez_server_app.course': {
            'Meta': {'object_name': 'Course'},
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 6, 29, 0, 0)'}),
            'description': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'blank': 'True'}),
            'faculty': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'faculty'", 'null': 'True', 'to': u"orm['nerdeez_server_app.Faculty']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'modified_data': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 6, 29, 0, 0)', 'auto_now': 'True', 'blank': 'True'}),
            'search_index': ('djorm_pgfulltext.fields.VectorField', [], {'default': "''", 'null': 'True', 'db_index': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '250'})
        },
        u'nerdeez_server_app.faculty': {
            'Meta': {'object_name': 'Faculty'},
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 6, 29, 0, 0)'}),
            'description': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'modified_data': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 6, 29, 0, 0)', 'auto_now': 'True', 'blank': 'True'}),
            'search_index': ('djorm_pgfulltext.fields.VectorField', [], {'default': "''", 'null': 'True', 'db_index': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'university': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'university'", 'null': 'True', 'to': u"orm['nerdeez_server_app.University']"})
        },
        u'nerdeez_server_app.university': {
            'Meta': {'object_name': 'University'},
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 6, 29, 0, 0)'}),
            'description': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'modified_data': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 6, 29, 0, 0)', 'auto_now': 'True', 'blank': 'True'}),
            'search_index': ('djorm_pgfulltext.fields.VectorField', [], {'default': "''", 'null': 'True', 'db_index': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '250'})
        }
    }

    complete_apps = ['nerdeez_server_app']