# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Job'
        db.create_table(u'mainsite_job', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal(u'mainsite', ['Job'])

        # Adding model 'ItemCategory'
        db.create_table(u'mainsite_itemcategory', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal(u'mainsite', ['ItemCategory'])

        # Adding model 'ItemType'
        db.create_table(u'mainsite_itemtype', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['mainsite.ItemCategory'])),
            ('job', self.gf('django.db.models.fields.related.ForeignKey')(related_name='itemcategory_job', null=True, to=orm['mainsite.Job'])),
        ))
        db.send_create_signal(u'mainsite', ['ItemType'])

        # Adding model 'Attribute'
        db.create_table(u'mainsite_attribute', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal(u'mainsite', ['Attribute'])

        # Adding model 'Panoplie'
        db.create_table(u'mainsite_panoplie', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal(u'mainsite', ['Panoplie'])

        # Adding model 'PanoplieAttribute'
        db.create_table(u'mainsite_panoplieattribute', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('panoplie', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['mainsite.Panoplie'])),
            ('attribute', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['mainsite.Attribute'])),
            ('value', self.gf('django.db.models.fields.IntegerField')()),
            ('no_of_items', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'mainsite', ['PanoplieAttribute'])

        # Adding model 'Recipe'
        db.create_table(u'mainsite_recipe', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('text', self.gf('django.db.models.fields.CharField')(max_length=1000)),
            ('size', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'mainsite', ['Recipe'])

        # Adding model 'Item'
        db.create_table(u'mainsite_item', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=5000, null=True)),
            ('image', self.gf('django.db.models.fields.CharField')(max_length=2048, null=True)),
            ('original_id', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['mainsite.ItemType'], null=True)),
            ('level', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('recipe', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['mainsite.Recipe'], null=True)),
            ('cost', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('range_min', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('range_max', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('crit_chance', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('crit_damage', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('failure', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('panoplie', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['mainsite.Panoplie'], null=True, on_delete=models.SET_NULL)),
        ))
        db.send_create_signal(u'mainsite', ['Item'])

        # Adding model 'AttributeValue'
        db.create_table(u'mainsite_attributevalue', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('item', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['mainsite.Item'])),
            ('attribute', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['mainsite.Attribute'])),
            ('min_value', self.gf('django.db.models.fields.IntegerField')()),
            ('max_value', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'mainsite', ['AttributeValue'])

        # Adding model 'AttributeCondition'
        db.create_table(u'mainsite_attributecondition', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('item', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['mainsite.Item'])),
            ('attribute', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['mainsite.Attribute'])),
            ('equality', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('required_value', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'mainsite', ['AttributeCondition'])

        # Adding model 'UpdateHistory'
        db.create_table(u'mainsite_updatehistory', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('started', self.gf('django.db.models.fields.DateTimeField')()),
            ('finished', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('using_cache', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'mainsite', ['UpdateHistory'])

        # Adding M2M table for field updated_items on 'UpdateHistory'
        m2m_table_name = db.shorten_name(u'mainsite_updatehistory_updated_items')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('updatehistory', models.ForeignKey(orm[u'mainsite.updatehistory'], null=False)),
            ('item', models.ForeignKey(orm[u'mainsite.item'], null=False))
        ))
        db.create_unique(m2m_table_name, ['updatehistory_id', 'item_id'])

        # Adding M2M table for field updated_panos on 'UpdateHistory'
        m2m_table_name = db.shorten_name(u'mainsite_updatehistory_updated_panos')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('updatehistory', models.ForeignKey(orm[u'mainsite.updatehistory'], null=False)),
            ('panoplie', models.ForeignKey(orm[u'mainsite.panoplie'], null=False))
        ))
        db.create_unique(m2m_table_name, ['updatehistory_id', 'panoplie_id'])

        # Adding model 'InvalidItem'
        db.create_table(u'mainsite_invaliditem', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('item', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['mainsite.Item'], null=True)),
            ('panoplie', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['mainsite.Panoplie'], null=True)),
            ('flag_date', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal(u'mainsite', ['InvalidItem'])


    def backwards(self, orm):
        # Deleting model 'Job'
        db.delete_table(u'mainsite_job')

        # Deleting model 'ItemCategory'
        db.delete_table(u'mainsite_itemcategory')

        # Deleting model 'ItemType'
        db.delete_table(u'mainsite_itemtype')

        # Deleting model 'Attribute'
        db.delete_table(u'mainsite_attribute')

        # Deleting model 'Panoplie'
        db.delete_table(u'mainsite_panoplie')

        # Deleting model 'PanoplieAttribute'
        db.delete_table(u'mainsite_panoplieattribute')

        # Deleting model 'Recipe'
        db.delete_table(u'mainsite_recipe')

        # Deleting model 'Item'
        db.delete_table(u'mainsite_item')

        # Deleting model 'AttributeValue'
        db.delete_table(u'mainsite_attributevalue')

        # Deleting model 'AttributeCondition'
        db.delete_table(u'mainsite_attributecondition')

        # Deleting model 'UpdateHistory'
        db.delete_table(u'mainsite_updatehistory')

        # Removing M2M table for field updated_items on 'UpdateHistory'
        db.delete_table(db.shorten_name(u'mainsite_updatehistory_updated_items'))

        # Removing M2M table for field updated_panos on 'UpdateHistory'
        db.delete_table(db.shorten_name(u'mainsite_updatehistory_updated_panos'))

        # Deleting model 'InvalidItem'
        db.delete_table(u'mainsite_invaliditem')


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
            'attributes': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'item_attribute'", 'null': 'True', 'through': u"orm['mainsite.AttributeValue']", 'to': u"orm['mainsite.Attribute']"}),
            'conditions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'item_condition'", 'null': 'True', 'through': u"orm['mainsite.AttributeCondition']", 'to': u"orm['mainsite.Attribute']"}),
            'cost': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'crit_chance': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'crit_damage': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '5000', 'null': 'True'}),
            'failure': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.CharField', [], {'max_length': '2048', 'null': 'True'}),
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
            'using_cache': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        }
    }

    complete_apps = ['mainsite']