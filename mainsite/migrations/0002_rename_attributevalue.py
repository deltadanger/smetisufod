# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        db.rename_table('mainsite_attributevalues', 'mainsite_attributevalue')


    def backwards(self, orm):
        db.rename_table('mainsite_attributevalue','mainsite_attributevalues')

    models = {
        u'mainsite.attribute': {
            'Meta': {'object_name': 'Attribute'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['mainsite.I18nString']"})
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
        u'mainsite.i18nstring': {
            'Meta': {'object_name': 'I18nString'},
            'en_us': ('django.db.models.fields.CharField', [], {'max_length': '9999', 'null': 'True'}),
            'fr_fr': ('django.db.models.fields.CharField', [], {'max_length': '9999', 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'mainsite.item': {
            'Meta': {'object_name': 'Item'},
            'attributes': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'item_attributes'", 'null': 'True', 'through': u"orm['mainsite.AttributeValue']", 'to': u"orm['mainsite.Attribute']"}),
            'conditions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'item_condition'", 'null': 'True', 'through': u"orm['mainsite.AttributeCondition']", 'to': u"orm['mainsite.Attribute']"}),
            'cost': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'craft': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['mainsite.Item']", 'null': 'True', 'through': u"orm['mainsite.Recipe']", 'symmetrical': 'False'}),
            'crit_chance': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'crit_damage': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'description': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'item_description'", 'null': 'True', 'to': u"orm['mainsite.I18nString']"}),
            'failure': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'has_valid_recipe': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'icon': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['mainsite.ItemType']", 'null': 'True'}),
            'level': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'name': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'item_name'", 'to': u"orm['mainsite.I18nString']"}),
            'range': ('django.db.models.fields.IntegerField', [], {'null': 'True'})
        },
        u'mainsite.itemcategory': {
            'Meta': {'object_name': 'ItemCategory'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'itemcategory_name'", 'to': u"orm['mainsite.I18nString']"})
        },
        u'mainsite.itemtype': {
            'Meta': {'object_name': 'ItemType'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['mainsite.ItemCategory']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'job': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'itemcategory_job'", 'null': 'True', 'to': u"orm['mainsite.Job']"}),
            'name': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['mainsite.I18nString']"})
        },
        u'mainsite.job': {
            'Meta': {'object_name': 'Job'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'job_name'", 'to': u"orm['mainsite.I18nString']"})
        },
        u'mainsite.recipe': {
            'Meta': {'object_name': 'Recipe'},
            'element': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'recipe_element'", 'to': u"orm['mainsite.Item']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'recipe_item'", 'to': u"orm['mainsite.Item']"}),
            'quantity': ('django.db.models.fields.IntegerField', [], {})
        }
    }

    complete_apps = ['mainsite']