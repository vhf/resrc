# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Language.name'
        db.add_column(u'language_language', 'name',
                      self.gf('django.db.models.fields.CharField')(default='asdf', max_length=30),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Language.name'
        db.delete_column(u'language_language', 'name')


    models = {
        u'language.language': {
            'Meta': {'object_name': 'Language'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'max_length': '7'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        }
    }

    complete_apps = ['language']