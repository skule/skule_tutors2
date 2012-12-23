# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Course'
        db.create_table('course_manage_course', (
            ('year', self.gf('django.db.models.fields.SmallIntegerField')()),
            ('course_code', self.gf('django.db.models.fields.CharField')(max_length=7, primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('course_manage', ['Course'])


    def backwards(self, orm):
        # Deleting model 'Course'
        db.delete_table('course_manage_course')


    models = {
        'course_manage.course': {
            'Meta': {'object_name': 'Course'},
            'course_code': ('django.db.models.fields.CharField', [], {'max_length': '7', 'primary_key': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'year': ('django.db.models.fields.SmallIntegerField', [], {})
        }
    }

    complete_apps = ['course_manage']