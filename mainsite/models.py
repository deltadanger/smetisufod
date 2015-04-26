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
        return unicode(self.text) + " ("+unicode(self.size)+" elements)"



class Item(BaseModel):
    name                = models.CharField(max_length=50)
    description         = models.CharField(max_length=5000, null=True)
    image               = models.CharField(max_length=2048, null=True)
    original_id         = models.IntegerField(null=True)
    type                = models.ForeignKey(ItemType, null=True)
    level               = models.IntegerField(null=True)
    attributes          = models.ManyToManyField(Attribute, related_name="item_attribute", through='AttributeValue', null=True)
    recipe              = models.ForeignKey(Recipe, null=True)
    conditions          = models.ManyToManyField(Attribute, related_name="item_condition", through='AttributeCondition', null=True)
    cost                = models.IntegerField(null=True)
    range_min           = models.IntegerField(null=True)
    range_max           = models.IntegerField(null=True)
    crit_chance         = models.IntegerField(null=True)
    crit_damage         = models.IntegerField(null=True)
    failure             = models.IntegerField(null=True)
    panoplie            = models.ForeignKey(Panoplie, null=True, on_delete=models.SET_NULL)
    
    def __unicode__(self):
        return unicode(self.name)

    @property
    def full_str(self):
        result = self.name + " (" + self.type.name + " - Level " + str(self.level) + " - id:" + str(self.original_id) + ")\n"
        result += "\n" + self.description + "\n"
        result += "\nImage: " + self.image + "\n"
        for a in self.attributevalue_set.all():
            result += "\n" + a.attribute.name + ": " + str(a.min_value) + "-" + str(a.max_value)
        
        result += "\n\nConditions\n"
        for c in self.attributecondition_set.all():
            result += c.attribute.name + " " +  c.equality + " " + str(c.required_value) + "\n"
        
        result += "\nCaracs\n"
        result += str(self.cost) + " PA ; " + str(self.range_min) + "-" + str(self.range_max) + " PO ; CC 1/" + str(self.crit_chance) + " (+" + str(self.crit_damage) + ")"
        
        result = result.encode('ascii', 'replace')
        
        result += "\n\nRecipe\n"
        result += str(self.recipe)
        
        result += "\n\nPanoplie\n"
        if self.panoplie:
            result += self.panoplie.name
        else:
            result += "None"
        
        result += "\n\n"
        return result

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
    using_cache = models.BooleanField(default=False)
    updated_items = models.ManyToManyField(Item)
    updated_panos = models.ManyToManyField(Panoplie)
    
    def __unicode__(self):
        return unicode(self.started) + " - " + unicode(self.finished) + " (" + str(self.updated_items.count() + self.updated_panos.count()) + ")"



class InvalidItem(BaseModel):
    item = models.ForeignKey(Item, null=True)
    panoplie = models.ForeignKey(Panoplie, null=True)
    origin = models.CharField(max_length=250, null=True)
    flag_date = models.DateTimeField()

    def __unicode__(self):
        if self.item:
            return unicode(self.item) + " - " + unicode(self.flag_date)
            
        return unicode(self.panoplie) + " - " + unicode(self.flag_date)
