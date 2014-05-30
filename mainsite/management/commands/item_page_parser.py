# -*- coding: utf-8 -*-
import re, logging

from HTMLParser import HTMLParser

from mainsite.models import Item, ItemType, ItemCategory, Attribute, AttributeValue, AttributeCondition, Recipe

log = logging.getLogger(__name__)

RE_LEVEL = re.compile("Level (\d+)")
RE_ATTRIBUTE = re.compile("(-?\d+)\.?\d*?( à (-?\d+)\.?\d*?)? (.*)")
RE_CONDITION = re.compile("(.+?) ([><=]) (\d+)")
RE_CARAC_PA = re.compile("PA : (\d{1,2})")
RE_CARAC_PO = re.compile("Portée : (\d{1,2})")
RE_CARAC_CC = re.compile("CC : 1/(\d{1,2})( \(\+(\d{1,2})\))?")
RE_CARAC_EC = re.compile("EC : 1/(\d{1,2})")
RE_RECIPE_ELEMENT_QUANTITY = re.compile("\+?\s+(\d) x ")
RE_ITEM_ID = re.compile(".*/(\d+)\.swf")

def get_attr(attrs, attr):
    for e in attrs:
        if e[0] == attr:
            return e[1]
    return ""

class ItemPageParser(HTMLParser):
    def __init__(self, item_type):
        HTMLParser.__init__(self)
        self.reset_vars()
        
        self.item = None
        self.item_type = item_type
        self.current_page = 0
        self.changed_items = []
        
    def reset_vars(self):
        self.has_changed = False
        self.current_item_attributes_dump = ""
        self.current_item_conditions_dump = ""
        
        self.get_name = False
        self.get_level = False
        self.in_desc = False
        self.get_desc = False
        self.in_caracs_block = False
        self.in_caracs_left = False
        self.get_attributes = False
        self.in_caracs_right = False
        self.in_conditions = False
        self.get_conditions = False
        self.in_caracs = False
        self.get_caracs = False
        self.in_recipe = False
        self.in_recipe_confirmed = False
        self.get_recipe = False
        self.recipe = ""
        self.in_pagination = False
        self.get_page = False
        
    
    def handle_starttag(self, tag, attrs):
        # Start of Item definition
        if tag == "div" and "middle_content" in get_attr(attrs, "class"):
            if self.item:
                self.has_changed |= self.item.type != self.item_type
                self.item.type = self.item_type
                
                self.has_changed |= self.current_item_attributes_dump != str(self.item.attributevalue_set.all())
                self.has_changed |= self.current_item_conditions_dump != str(self.item.attributecondition_set.all())
                
                self.item.save()
                
                if self.has_changed:
                    self.changed_items.append(self.item)
                
            self.reset_vars()
        
        
        # Name of Item
        if tag == "h2" and "title_element" in get_attr(attrs, "class"):
            self.get_name = True
        
        # Level of Item
        if tag == "span" and "level_element" in get_attr(attrs, "class"):
            self.get_level = True
        
        # Original Id of Item, for flash image display
        if tag == "param" and "flashvars" in get_attr(attrs, "name"):
            match = RE_ITEM_ID.match(get_attr(attrs, "value"))
            
            if match:
                self.item.original_id = int(match.group(1))
        
        # Description of Item
        if tag == "div" and "desc" in get_attr(attrs, "class"):
            self.in_desc = True
        
        if self.in_desc and tag == "span":
            self.get_desc = True
        
        # Attributes of Item
        if tag == "div" and "element_carac" in get_attr(attrs, "class"):
            self.in_caracs_block = True
            
        if self.in_caracs_block and tag == "div" and "element_carac_left" in get_attr(attrs, "class"):
            self.in_caracs_left = True
        
        if self.in_caracs_left and tag == "li":
            self.get_attributes = True
        
        # Conditions of Item
        if self.in_caracs_block and tag == "div" and "element_carac_right" in get_attr(attrs, "class"):
            self.in_caracs_left = False
            self.get_attributes = False
            self.in_caracs_right = True
        
        if self.in_conditions and tag == "ul":
            self.get_conditions = True
        
        # Caracteristics of Item
        if self.in_caracs and tag == "ul":
            self.get_caracs = True
        
        # Recipe of Item
        if tag == "div" and "element_carac_block1" in get_attr(attrs, "class"):
            self.in_caracs_block = False
            self.in_caracs_left = False
            self.get_attributes = False
            self.in_caracs_right = False
            self.get_conditions = False
            self.get_caracs = False
            
            self.in_recipe = True
        
        if self.in_recipe_confirmed and tag == "p":
            self.get_recipe = True
        
        
        # Current Page number, used for last-page-check
        if tag == "div" and "pagination" in get_attr(attrs, "class"):
            self.in_pagination = True
        
        if self.in_pagination and tag == "span" and "on" in get_attr(attrs, "class"):
            self.get_page = True
        
    def handle_data(self, data):
        if self.get_name:
            self.item, created = Item.objects.get_or_create(name=data)
            log.debug("Item: " + data + " ("+str(created)+")")
            self.has_changed |= created
            
            self.current_item_attributes_dump = str(self.item.attributevalue_set.all())
            self.item.attributevalue_set.all().delete()
            
            self.current_item_conditions_dump = str(self.item.attributecondition_set.all())
            self.item.attributecondition_set.all().delete()
        
        if self.get_level:
            match = RE_LEVEL.match(data)
            if match:
                self.has_changed |= self.item.level != int(match.group(1))
                self.item.level = match.group(1)
        
        if self.get_desc:
            self.has_changed |= self.item.description != unicode(data.decode("utf-8"))
            self.item.description = data
        
        if self.get_attributes:
            match = RE_ATTRIBUTE.match(data)
            if match:
                attr = match.group(4)
                min = match.group(1)
                max = match.group(3)
                if not max:
                    max = min
                if int(min) < 0 and int(max) > 0:
                    max = "-"+max
                
                # if not Attribute.objects.get_if_exist(name=attr):
                    # log.debug(match.groups())
                    # raise Exception("Weird attribute:" + attr + " on " + self.item.name)
                
                attr, created = Attribute.objects.get_or_create(name=attr)
                
                AttributeValue.objects.get_or_create(item=self.item, attribute=attr, min_value=int(min), max_value=int(max))
        
        if self.in_caracs_right and "Conditions :" in data:
            self.in_conditions = True
            
        if self.get_conditions:
            match = RE_CONDITION.match(data)
            if match:
                attr, equality, value = match.groups()
                attr, created = Attribute.objects.get_or_create(name=attr)
                
                AttributeCondition.objects.get_or_create(item=self.item, attribute=attr, equality=equality, required_value=value)
         
        if self.in_caracs_right and "Caractéristiques" in data:
            self.in_caracs = True
            
        if self.get_caracs:
            pa = RE_CARAC_PA.match(data)
            po = RE_CARAC_PO.match(data)
            cc = RE_CARAC_CC.match(data)
            ec = RE_CARAC_EC.match(data)
            
            if pa:
                self.has_changed |= self.item.cost != int(pa.group(1))
                self.item.cost = int(pa.group(1))
                
            if po:
                self.has_changed |= self.item.range != int(po.group(1))
                self.item.range = int(po.group(1))
            
            if cc:
                self.has_changed |= self.item.crit_chance != int(cc.group(1))
                self.item.crit_chance = int(cc.group(1))
                if cc.group(3):
                    self.has_changed |= self.item.crit_damage != int(cc.group(3))
                    self.item.crit_damage = int(cc.group(3))
                
            if ec:
                self.has_changed |= self.item.failure != int(ec.group(1))
                self.item.failure = int(ec.group(1))
        
        if self.in_recipe and "Craft :" in data:
            self.in_recipe_confirmed = True
        
        if self.get_recipe:
            self.recipe += re.sub("\s+", " ", data)
        
        if self.get_page:
            self.current_page = int(data)
        
    def handle_endtag(self, tag):
        if self.get_page and tag == "span":
            self.get_page = False
            self.in_pagination = False
        
        if self.in_recipe and tag == "p":
            self.get_recipe = False
            self.in_recipe_confirmed = False
            self.in_recipe = False
            
            recipe = self.item.recipe
            if not recipe:
                recipe = Recipe()
            
            recipe.text = self.recipe
            recipe.size = self.recipe.count(" x ")
            recipe.save()
            self.has_changed |= self.item.recipe != recipe
            self.item.recipe = recipe
            
        if self.get_caracs and tag == "ul":
            self.get_caracs = False
            self.in_caracs_right = False
            self.in_caracs_block = False
            
        if self.get_conditions and tag == "ul":
            self.get_conditions = False
            self.in_conditions = False
        
        if self.get_attributes and tag == "ul":
            self.get_attributes = False
            self.in_caracs_left = False
            self.in_caracs_block = False
            
        if self.get_desc and tag == "span":
            self.get_desc = False
            self.in_desc = False
        
        if self.get_name and tag == "h2":
            self.get_name = False
        
        if self.get_level and tag == "span":
            self.get_level = False
        