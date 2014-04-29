# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'I18nString'
        db.create_table(u'mainsite_i18nstring', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('fr_fr', self.gf('django.db.models.fields.CharField')(max_length=9999, null=True)),
            ('en_us', self.gf('django.db.models.fields.CharField')(max_length=9999, null=True)),
        ))
        db.send_create_signal(u'mainsite', ['I18nString'])

        # Adding model 'Job'
        db.create_table(u'mainsite_job', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.related.ForeignKey')(related_name='job_name', to=orm['mainsite.I18nString'])),
        ))
        db.send_create_signal(u'mainsite', ['Job'])

        # Adding model 'ItemCategory'
        db.create_table(u'mainsite_itemcategory', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.related.ForeignKey')(related_name='itemcategory_name', to=orm['mainsite.I18nString'])),
        ))
        db.send_create_signal(u'mainsite', ['ItemCategory'])

        # Adding model 'ItemType'
        db.create_table(u'mainsite_itemtype', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['mainsite.I18nString'])),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['mainsite.ItemCategory'])),
            ('job', self.gf('django.db.models.fields.related.ForeignKey')(related_name='itemcategory_job', null=True, to=orm['mainsite.Job'])),
        ))
        db.send_create_signal(u'mainsite', ['ItemType'])

        # Adding model 'Attribute'
        db.create_table(u'mainsite_attribute', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['mainsite.I18nString'])),
        ))
        db.send_create_signal(u'mainsite', ['Attribute'])

        # Adding model 'Item'
        db.create_table(u'mainsite_item', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.related.ForeignKey')(related_name='item_name', to=orm['mainsite.I18nString'])),
            ('description', self.gf('django.db.models.fields.related.ForeignKey')(related_name='item_description', null=True, to=orm['mainsite.I18nString'])),
            ('icon', self.gf('django.db.models.fields.CharField')(max_length=255, null=True)),
            ('item_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['mainsite.ItemType'], null=True)),
            ('level', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('has_valid_recipe', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('cost', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('range', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('crit_chance', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('crit_damage', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('failure', self.gf('django.db.models.fields.IntegerField')(null=True)),
        ))
        db.send_create_signal(u'mainsite', ['Item'])

        # Adding model 'AttributeValues'
        db.create_table(u'mainsite_attributevalues', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('item', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['mainsite.Item'])),
            ('attribute', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['mainsite.Attribute'])),
            ('min_value', self.gf('django.db.models.fields.IntegerField')()),
            ('max_value', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'mainsite', ['AttributeValues'])

        # Adding model 'AttributeCondition'
        db.create_table(u'mainsite_attributecondition', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('item', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['mainsite.Item'])),
            ('attribute', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['mainsite.Attribute'])),
            ('equality', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('required_value', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'mainsite', ['AttributeCondition'])

        # Adding model 'Recipe'
        db.create_table(u'mainsite_recipe', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('item', self.gf('django.db.models.fields.related.ForeignKey')(related_name='recipe_item', to=orm['mainsite.Item'])),
            ('element', self.gf('django.db.models.fields.related.ForeignKey')(related_name='recipe_element', to=orm['mainsite.Item'])),
            ('quantity', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'mainsite', ['Recipe'])


    def backwards(self, orm):
        # Deleting model 'I18nString'
        db.delete_table(u'mainsite_i18nstring')

        # Deleting model 'Job'
        db.delete_table(u'mainsite_job')

        # Deleting model 'ItemCategory'
        db.delete_table(u'mainsite_itemcategory')

        # Deleting model 'ItemType'
        db.delete_table(u'mainsite_itemtype')

        # Deleting model 'Attribute'
        db.delete_table(u'mainsite_attribute')

        # Deleting model 'Item'
        db.delete_table(u'mainsite_item')

        # Deleting model 'AttributeValues'
        db.delete_table(u'mainsite_attributevalues')

        # Deleting model 'AttributeCondition'
        db.delete_table(u'mainsite_attributecondition')

        # Deleting model 'Recipe'
        db.delete_table(u'mainsite_recipe')


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
        u'mainsite.attributevalues': {
            'Meta': {'object_name': 'AttributeValues'},
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
            'attributes': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'item_attributes'", 'null': 'True', 'through': u"orm['mainsite.AttributeValues']", 'to': u"orm['mainsite.Attribute']"}),
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