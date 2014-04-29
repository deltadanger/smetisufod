# -*- coding: utf-8 -*-
import re, urllib

from HTMLParser import HTMLParser

from mainsite.models import I18nString, Item, ItemType, ItemCategory, Attribute, AttributeValue, AttributeCondition, Recipe


RE_LEVEL = re.compile("Level (\d+)")
RE_ATTRIBUTE = re.compile("(-?\d+)( à (-?\d+))? (.*)")
RE_CONDITION = re.compile("(.+?) ([><=]) (\d+)")
RE_CARAC_PA = re.compile("PA : (\d{1,2})")
RE_CARAC_PO = re.compile("Portée : (\d{1,2})")
RE_CARAC_CC = re.compile("CC : 1/(\d{1,2})( \(\+(\d{1,2})\))?")
RE_CARAC_EC = re.compile("EC : 1/(\d{1,2})")
RE_RECIPE_ELEMENT_QUANTITY = re.compile("\+?\s*(\d) x ")

def get_attr(attrs, attr):
    for e in attrs:
        if e[0] == attr:
            return e[1]
    return ""

class ItemPageParser(HTMLParser):
    def __init__(self, item_type):
        HTMLParser.__init__(self)
        self.reset_vars()
        
        self.data = []
        self.item = None
        self.item_type = item_type
        self.current_page = 0
        
    def reset_vars(self):
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
        self.get_recipe = False
        self.recipe = None
        self.invalid_recipe = False
        self.in_pagination = False
        self.get_page = False
        
    
    def handle_starttag(self, tag, attrs):
        if tag == "div" and "middle_content" in get_attr(attrs, "class"):
            if self.item:
                if self.invalid_recipe:
                    Recipe.objects.filter(item=self.item).delete()
                    self.item.has_valid_recipe = False
                self.item.item_type = self.item_type
                self.item.save()
                self.data.append(self.item)
            self.reset_vars()
        
        
        if tag == "h2" and "title_element" in get_attr(attrs, "class"):
            self.get_name = True
        
        if tag == "span" and "level_element" in get_attr(attrs, "class"):
            self.get_level = True
        
        
        if tag == "div" and "desc" in get_attr(attrs, "class"):
            self.in_desc = True
        
        if self.in_desc and tag == "span":
            self.get_desc = True
        
        
        if tag == "div" and "element_carac" in get_attr(attrs, "class"):
            self.in_caracs_block = True
            
        if self.in_caracs_block and tag == "div" and "element_carac_left" in get_attr(attrs, "class"):
            self.in_caracs_left = True
        
        if self.in_caracs_block and tag == "ul":
            self.get_attributes = True
        
        
        if self.in_caracs_block and tag == "div" and "element_carac_right" in get_attr(attrs, "class"):
            self.in_caracs_left = False
            self.get_attributes = False
            self.in_caracs_right = True
        
        if self.in_conditions and tag == "ul":
            self.get_conditions = True
        
        if self.in_caracs and tag == "ul":
            self.get_caracs = True
        
        
        if tag == "div" and "element_carac_block1" in get_attr(attrs, "class"):
            self.in_recipe = True
        
        if self.in_recipe and tag == "p":
            self.get_recipe = True
        
        
        
        if tag == "div" and "pagination" in get_attr(attrs, "class"):
            self.in_pagination = True
        
        if self.in_pagination and tag == "span" and "on" in get_attr(attrs, "class"):
            self.get_page = True
        
    def handle_data(self, data):
        if self.get_name:
            name, created = I18nString.objects.get_or_create(fr_fr=data)
            self.item, created = Item.objects.get_or_create(name=name)
        
        if self.get_level:
            match = RE_LEVEL.match(data)
            if match:
                self.item.level = match.group(1)
        
        if self.get_desc:
            self.item.description, created = I18nString.objects.get_or_create(fr_fr=data)
        
        if self.get_attributes:
            match = RE_ATTRIBUTE.match(data)
            if match:
                attr, created = I18nString.objects.get_or_create(fr_fr=match.group(4))
                min = match.group(1)
                max = match.group(3)
                if not max:
                    max = min
                if int(min) < 0 and int(max) > 0:
                    max = "-"+max
                
                attr, created = Attribute.objects.get_or_create(name=attr)
                
                AttributeValue.objects.get_or_create(item=self.item, attribute=attr, min_value=int(min), max_value=int(max))
        
        if self.in_caracs_right and "Conditions :" in data:
            self.in_conditions = True
            
        if self.get_conditions:
            match = RE_CONDITION.match(data)
            if match:
                attr, equality, value = match.groups()
                attr, created = I18nString.objects.get_or_create(fr_fr=attr)
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
                self.item.cost = int(pa.group(1))
                
            if po:
                self.item.range = int(po.group(1))
            
            if cc:
                self.item.crit_chance = int(cc.group(1))
                if cc.group(3):
                    self.item.crit_damage = int(cc.group(3))
                
            if ec:
                self.item.failure = int(ec.group(1))
        
        if self.get_recipe:
            if not self.recipe:
                self.recipe = Recipe(item=self.item)
            
            match = RE_RECIPE_ELEMENT_QUANTITY.match(data)
            if match:
                self.recipe.quantity = int(match.group(1))
                try:
                    self.recipe.save()
                    self.recipe = None
                except Exception as e:
                    if "IntegrityError" not in str(type(e)):
                        raise
            else:
                name = I18nString.objects.get_if_exist(fr_fr=data)
                item = Item.objects.get_if_exist(name=name)
                if item:
                    self.recipe.element = item
                    try:
                        self.recipe.save()
                        self.recipe = None
                    except Exception as e:
                        if "IntegrityError" not in str(type(e)):
                            raise
                else:
                    self.recipe = None
                    self.invalid_recipe = True
        
        
        if self.get_page:
            self.current_page = int(data)
        
    def handle_endtag(self, tag):
        if self.get_page and tag == "span":
            self.get_page = False
            self.in_pagination = False
        
        if self.get_recipe and tag == "p":
            self.get_recipe = False
            self.in_recipe = False
            
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
        