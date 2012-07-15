# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Tag'
        db.create_table('metablog_tag', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=24)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=24)),
        ))
        db.send_create_signal('metablog', ['Tag'])

        # Adding model 'Post'
        db.create_table('metablog_post', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50)),
            ('post_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified_date', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('status', self.gf('django.db.models.fields.SmallIntegerField')()),
            ('prev_post', self.gf('django.db.models.fields.related.OneToOneField')(blank=True, related_name='next', unique=True, null=True, to=orm['metablog.Post'])),
            ('next_post', self.gf('django.db.models.fields.related.OneToOneField')(blank=True, related_name='prev', unique=True, null=True, to=orm['metablog.Post'])),
            ('text', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('metablog', ['Post'])

        # Adding M2M table for field tags on 'Post'
        db.create_table('metablog_post_tags', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('post', models.ForeignKey(orm['metablog.post'], null=False)),
            ('tag', models.ForeignKey(orm['metablog.tag'], null=False))
        ))
        db.create_unique('metablog_post_tags', ['post_id', 'tag_id'])

        # Adding model 'Category'
        db.create_table('metablog_category', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('tag', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['metablog.Tag'], unique=True)),
            ('long_name', self.gf('django.db.models.fields.CharField')(max_length=32)),
        ))
        db.send_create_signal('metablog', ['Category'])


    def backwards(self, orm):
        # Deleting model 'Tag'
        db.delete_table('metablog_tag')

        # Deleting model 'Post'
        db.delete_table('metablog_post')

        # Removing M2M table for field tags on 'Post'
        db.delete_table('metablog_post_tags')

        # Deleting model 'Category'
        db.delete_table('metablog_category')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'metablog.category': {
            'Meta': {'object_name': 'Category'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'long_name': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'tag': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['metablog.Tag']", 'unique': 'True'})
        },
        'metablog.post': {
            'Meta': {'object_name': 'Post'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'next_post': ('django.db.models.fields.related.OneToOneField', [], {'blank': 'True', 'related_name': "'prev'", 'unique': 'True', 'null': 'True', 'to': "orm['metablog.Post']"}),
            'post_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'prev_post': ('django.db.models.fields.related.OneToOneField', [], {'blank': 'True', 'related_name': "'next'", 'unique': 'True', 'null': 'True', 'to': "orm['metablog.Post']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'status': ('django.db.models.fields.SmallIntegerField', [], {}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['metablog.Tag']", 'symmetrical': 'False'}),
            'text': ('django.db.models.fields.TextField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
        'metablog.tag': {
            'Meta': {'object_name': 'Tag'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '24'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '24'})
        }
    }

    complete_apps = ['metablog']