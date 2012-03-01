# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Deleting field 'Picture.thumbnail'
        db.delete_column('gallery_picture', 'thumbnail')

        # Deleting field 'Picture.viewable'
        db.delete_column('gallery_picture', 'viewable')


    def backwards(self, orm):
        
        # Adding field 'Picture.thumbnail'
        db.add_column('gallery_picture', 'thumbnail', self.gf('django.db.models.fields.files.ImageField')(default='', max_length=100), keep_default=False)

        # Adding field 'Picture.viewable'
        db.add_column('gallery_picture', 'viewable', self.gf('django.db.models.fields.files.ImageField')(default='', max_length=100), keep_default=False)


    models = {
        'gallery.gallery': {
            'Meta': {'ordering': "('order',)", 'object_name': 'Gallery'},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'description': ('ckeditor.fields.HTMLField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'order': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'parent_gallery': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['gallery.Gallery']", 'null': 'True', 'blank': 'True'}),
            'published': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50', 'db_index': 'True'})
        },
        'gallery.picture': {
            'Meta': {'ordering': "('order',)", 'object_name': 'Picture'},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'description': ('ckeditor.fields.HTMLField', [], {'null': 'True', 'blank': 'True'}),
            'gallery': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['gallery.Gallery']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'order': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'original': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50', 'db_index': 'True'})
        }
    }

    complete_apps = ['gallery']
