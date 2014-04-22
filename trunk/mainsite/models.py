from django.db import models


class I18nString(models.Model):
    fr_fr = models.CharField(max_length=9999, null=True)
    en_us = models.CharField(max_length=9999, null=True)
    
    def __repr__(self):
        return self.fr_fr



class ItemCategory(models.Model):
    name = models.ForeignKey(I18nString)
    job = models.ForeignKey(I18nString)
    
    def __repr__(self):
        return self.name

class ItemType(models.Model):
    name = models.ForeignKey(I18nString)
    category = models.ForeignKey(ItemCategory)
    
    def __repr__(self):
        return self.name

class Attribute(models.Model):
    name = models.ForeignKey(I18nString)
    
    def __repr__(self):
        return self.name

class Item(models.Model):
    name            = models.ForeignKey(I18nString)
    description     = models.ForeignKey(I18nString, null=True)
    icon            = models.CharField(max_length=255, null=True)
    item_type       = models.ForeignKey(ItemType, null=True)
    level           = models.IntegerField()
    attributes      = models.ManyToManyField(Attribute, through='AttributeValues', null=True)
    craft           = models.ManyToManyField("Item", through='Recipe', symmetrical=False, null=True)
    condition       = models.ManyToManyField(Attribute, through='AttributeCondition', null=True)
    cost            = models.IntegerField()
    range           = models.IntegerField()
    critical        = models.IntegerField()
    failure         = models.IntegerField()
    
    def __repr__(self):
        return self.name

class AttributeValues(models.Model):
    item = models.ForeignKey(Item)
    attribute = models.ForeignKey(Attribute)
    min_value = models.IntegerField()
    max_value = models.IntegerField()

class AttributeCondition(models.Model):
    item = models.ForeignKey(Item)
    attribute = models.ForeignKey(Attribute)
    required_value = models.IntegerField()

class Recipe(models.Model):
    item = models.ForeignKey(Item)
    element = models.ForeignKey(Item)
    quantity = models.IntegerField()

