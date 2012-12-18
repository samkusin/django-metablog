# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Link'
        db.create_table('metablog_link', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('tag', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['metablog.Tag'])),
            ('rank', self.gf('django.db.models.fields.SmallIntegerField')()),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200)),
        ))
        db.send_create_signal('metablog', ['Link'])

        # Adding index on 'Post', fields ['status']
        db.create_index('metablog_post', ['status'])


    def backwards(self, orm):
        # Removing index on 'Post', fields ['status']
        db.delete_index('metablog_post', ['status'])

        # Deleting model 'Link'
        db.delete_table('metablog_link')


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
        'metablog.link': {
            'Meta': {'object_name': 'Link'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'rank': ('django.db.models.fields.SmallIntegerField', [], {}),
            'tag': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['metablog.Tag']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        },
        'metablog.post': {
            'Meta': {'object_name': 'Post'},
            'atj_word_count': ('django.db.models.fields.SmallIntegerField', [], {'default': '150'}),
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'next_post': ('django.db.models.fields.related.OneToOneField', [], {'blank': 'True', 'related_name': "'prev'", 'unique': 'True', 'null': 'True', 'to': "orm['metablog.Post']"}),
            'post_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'prev_post': ('django.db.models.fields.related.OneToOneField', [], {'blank': 'True', 'related_name': "'next'", 'unique': 'True', 'null': 'True', 'to': "orm['metablog.Post']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'status': ('django.db.models.fields.SmallIntegerField', [], {'db_index': 'True'}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['metablog.Tag']", 'symmetrical': 'False'}),
            'text': ('django.db.models.fields.TextField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
        'metablog.slide': {
            'Meta': {'object_name': 'Slide'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'media_type': ('django.db.models.fields.SmallIntegerField', [], {}),
            'media_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'post': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['metablog.Post']", 'null': 'True', 'on_delete': 'models.SET_NULL', 'blank': 'True'}),
            'thumbnail_text': ('django.db.models.fields.CharField', [], {'max_length': '32'})
        },
        'metablog.slideshow': {
            'Meta': {'object_name': 'SlideShow'},
            'date': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '32'}),
            'slides': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['metablog.Slide']", 'through': "orm['metablog.SlideShowSlide']", 'symmetrical': 'False'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '128', 'blank': 'True'})
        },
        'metablog.slideshowslide': {
            'Meta': {'ordering': "('order',)", 'object_name': 'SlideShowSlide'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'slide': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['metablog.Slide']"}),
            'slideshow': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['metablog.SlideShow']"})
        },
        'metablog.tag': {
            'Meta': {'object_name': 'Tag'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '24'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '24'})
        }
    }

    complete_apps = ['metablog']