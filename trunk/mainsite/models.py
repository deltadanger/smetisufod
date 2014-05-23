from django.db import models

class AdvancedManager(models.Manager):
    """Contains advanced functions, but nothing related to StandardLookup tables, such as get_if_exist(**kwargs)"""
    
    def get_if_exist(self, **kwargs):
        """Returns the matching object if it uniquely exists, None otherwise"""
        try:
            return self.get(**kwargs)
        except (self.model.DoesNotExist, self.model.MultipleObjectsReturned) as e:
            return None
    


class BaseModel(models.Model):
    objects = AdvancedManager()
    
    class Meta:
        abstract = True


class Job(BaseModel):
    name = models.CharField(max_length=50)
    
    def __unicode__(self):
        return unicode(self.name)

class ItemCategory(BaseModel):
    name = models.CharField(max_length=50)
    
    def __unicode__(self):
        return unicode(self.name)

class ItemType(BaseModel):
    name = models.CharField(max_length=50)
    category = models.ForeignKey(ItemCategory)
    job = models.ForeignKey(Job, related_name="itemcategory_job", null=True)
    
    def __unicode__(self):
        return unicode(self.name)

class Attribute(BaseModel):
    name = models.CharField(max_length=50)
    
    def __unicode__(self):
        return unicode(self.name)


class Panoplie(BaseModel):
    name = models.CharField(max_length=50)
    attributes = models.ManyToManyField(Attribute, through='PanoplieAttribute', null=True)
    
    def __unicode__(self):
        return unicode(self.name)

class PanoplieAttribute(BaseModel):
    panoplie = models.ForeignKey(Panoplie)
    attribute = models.ForeignKey(Attribute)
    value = models.IntegerField()
    no_of_items = models.IntegerField()
    
    def __unicode__(self):
        return unicode(self.panoplie) + "-" + unicode(self.value) + " " + unicode(self.attribute) + "(" + str(self.no_of_items) + ")"


class Recipe(BaseModel):
    text = models.CharField(max_length=1000)
    size = models.IntegerField()
    
    def __unicode__(self):
        return unicode(self.text) + " ("+str(self.size)+" elements)"



class Item(BaseModel):
    name                = models.CharField(max_length=50)
    description         = models.CharField(max_length=5000)
    original_id         = models.IntegerField(null=True)
    type                = models.ForeignKey(ItemType, null=True)
    level               = models.IntegerField(null=True)
    attribute           = models.ManyToManyField(Attribute, related_name="item_attribute", through='AttributeValue', null=True)
    recipe              = models.ForeignKey(Recipe, null=True)
    condition           = models.ManyToManyField(Attribute, related_name="item_condition", through='AttributeCondition', null=True)
    cost                = models.IntegerField(null=True)
    range               = models.IntegerField(null=True)
    crit_chance         = models.IntegerField(null=True)
    crit_damage         = models.IntegerField(null=True)
    failure             = models.IntegerField(null=True)
    panoplie            = models.ForeignKey(Panoplie, null=True, on_delete=models.SET_NULL)
    
    def __unicode__(self):
        return unicode(self.name)

class AttributeValue(BaseModel):
    item = models.ForeignKey(Item)
    attribute = models.ForeignKey(Attribute)
    min_value = models.IntegerField()
    max_value = models.IntegerField()
    
    def __unicode__(self):
        return unicode(self.item) + "-" + unicode(self.attribute) + "("+unicode(self.min_value)+ "-"+unicode(self.max_value)+")"

class AttributeCondition(BaseModel):
    item = models.ForeignKey(Item)
    attribute = models.ForeignKey(Attribute)
    equality = models.CharField(max_length=1)
    required_value = models.IntegerField()
    
    def __unicode__(self):
        return unicode(self.item) + "-" + unicode(self.attribute) + unicode(self.equality) + unicode(self.required_value)




class UpdateHistory(BaseModel):
    started = models.DateTimeField()
    finished = models.DateTimeField(null=True)
    using_cache = models.BooleanField()
    updated_items = models.ManyToManyField(Item)
    updated_panos = models.ManyToManyField(Panoplie)
    
    def __unicode__(self):
        return unicode(self.started) + " - " + unicode(self.finished) + " (" + str(self.updated_items.count() + self.updated_panos.count()) + ")"



class InvalidItem(BaseModel):
    item = models.ForeignKey(Item, null=True)
    panoplie = models.ForeignKey(Panoplie, null=True)
    flag_date = models.DateTimeField()

    def __unicode__(self):
        if self.item:
            return unicode(self.item) + " - " + unicode(self.flag_date)
            
        return unicode(self.panoplie) + " - " + unicode(self.flag_date)
