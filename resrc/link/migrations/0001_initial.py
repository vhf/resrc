# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Link'
        db.create_table(u'link_link', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=120)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=255)),
            ('hash2', self.gf('django.db.models.fields.CharField')(max_length=11)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('pubdate', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('upvotes', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('votes_h00', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('votes_h02', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('votes_h04', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('votes_h06', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('votes_h08', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('votes_h10', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('votes_h12', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('votes_h14', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('votes_h16', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('votes_h18', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('votes_h20', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('votes_h22', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('score_h24', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal(u'link', ['Link'])


    def backwards(self, orm):
        # Deleting model 'Link'
        db.delete_table(u'link_link')


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
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'link.link': {
            'Meta': {'object_name': 'Link'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'hash2': ('django.db.models.fields.CharField', [], {'max_length': '11'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pubdate': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'score_h24': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '255'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '120'}),
            'upvotes': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'votes_h00': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'votes_h02': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'votes_h04': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'votes_h06': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'votes_h08': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'votes_h10': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'votes_h12': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'votes_h14': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'votes_h16': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'votes_h18': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'votes_h20': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'votes_h22': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        u'taggit.tag': {
            'Meta': {'object_name': 'Tag'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '100'})
        },
        u'taggit.taggeditem': {
            'Meta': {'object_name': 'TaggedItem'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'taggit_taggeditem_tagged_items'", 'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.IntegerField', [], {'db_index': 'True'}),
            'tag': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'taggit_taggeditem_items'", 'to': u"orm['taggit.Tag']"})
        }
    }

    complete_apps = ['link']