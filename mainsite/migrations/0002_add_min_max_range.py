# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Item.range'
        db.delete_column(u'mainsite_item', 'range')

        # Adding field 'Item.range_min'
        db.add_column(u'mainsite_item', 'range_min',
                      self.gf('django.db.models.fields.IntegerField')(null=True),
                      keep_default=False)

        # Adding field 'Item.range_max'
        db.add_column(u'mainsite_item', 'range_max',
                      self.gf('django.db.models.fields.IntegerField')(null=True),
                      keep_default=False)


    def backwards(self, orm):
        # Adding field 'Item.range'
        db.add_column(u'mainsite_item', 'range',
                      self.gf('django.db.models.fields.IntegerField')(null=True),
                      keep_default=False)

        # Deleting field 'Item.range_min'
        db.delete_column(u'mainsite_item', 'range_min')

        # Deleting field 'Item.range_max'
        db.delete_column(u'mainsite_item', 'range_max')


    models = {
        u'mainsite.attribute': {
            'Meta': {'object_name': 'Attribute'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'mainsite.attributecondition': {
            'Meta': {'object_name': 'AttributeCondition'},
            'attribute': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['mainsite.Attribute']"}),
            'equality': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['mainsite.Item']"}),
            'required_value': ('django.db.models.fields.IntegerField', [], {})
        },
        u'mainsite.attributevalue': {
            'Meta': {'object_name': 'AttributeValue'},
            'attribute': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['mainsite.Attribute']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['mainsite.Item']"}),
            'max_value': ('django.db.models.fields.IntegerField', [], {}),
            'min_value': ('django.db.models.fields.IntegerField', [], {})
        },
        u'mainsite.invaliditem': {
            'Meta': {'object_name': 'InvalidItem'},
            'flag_date': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['mainsite.Item']", 'null': 'True'}),
            'panoplie': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['mainsite.Panoplie']", 'null': 'True'})
        },
        u'mainsite.item': {
            'Meta': {'object_name': 'Item'},
            'attribute': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'item_attribute'", 'null': 'True', 'through': u"orm['mainsite.AttributeValue']", 'to': u"orm['mainsite.Attribute']"}),
            'condition': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'item_condition'", 'null': 'True', 'through': u"orm['mainsite.AttributeCondition']", 'to': u"orm['mainsite.Attribute']"}),
            'cost': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'crit_chance': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'crit_damage': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '5000'}),
            'failure': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'original_id': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'panoplie': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['mainsite.Panoplie']", 'null': 'True', 'on_delete': 'models.SET_NULL'}),
            'range_max': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'range_min': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'recipe': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['mainsite.Recipe']", 'null': 'True'}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['mainsite.ItemType']", 'null': 'True'})
        },
        u'mainsite.itemcategory': {
            'Meta': {'object_name': 'ItemCategory'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'mainsite.itemtype': {
            'Meta': {'object_name': 'ItemType'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['mainsite.ItemCategory']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'job': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'itemcategory_job'", 'null': 'True', 'to': u"orm['mainsite.Job']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'mainsite.job': {
            'Meta': {'object_name': 'Job'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'mainsite.panoplie': {
            'Meta': {'object_name': 'Panoplie'},
            'attributes': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['mainsite.Attribute']", 'null': 'True', 'through': u"orm['mainsite.PanoplieAttribute']", 'symmetrical': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'mainsite.panoplieattribute': {
            'Meta': {'object_name': 'PanoplieAttribute'},
            'attribute': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['mainsite.Attribute']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'no_of_items': ('django.db.models.fields.IntegerField', [], {}),
            'panoplie': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['mainsite.Panoplie']"}),
            'value': ('django.db.models.fields.IntegerField', [], {})
        },
        u'mainsite.recipe': {
            'Meta': {'object_name': 'Recipe'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'size': ('django.db.models.fields.IntegerField', [], {}),
            'text': ('django.db.models.fields.CharField', [], {'max_length': '1000'})
        },
        u'mainsite.updatehistory': {
            'Meta': {'object_name': 'UpdateHistory'},
            'finished': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'started': ('django.db.models.fields.DateTimeField', [], {}),
            'updated_items': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['mainsite.Item']", 'symmetrical': 'False'}),
            'updated_panos': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['mainsite.Panoplie']", 'symmetrical': 'False'}),
            'using_cache': ('django.db.models.fields.BooleanField', [], {})
        }
    }

    complete_apps = ['mainsite']