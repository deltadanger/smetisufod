# -*- coding: utf-8 -*-
from HTMLParser import HTMLParser
import re, logging

from rebuild_db import printItems
from mainsite.models import Item, Attribute, AttributeValue, AttributeCondition, Recipe, \
    ItemType


log = logging.getLogger(__name__)

RE_ITEM_ID = re.compile("fr/mmorpg/encyclopedie/[a-z]+/(.*)")

RE_LEVEL = re.compile("Niveau : (\d+)")
RE_ATTRIBUTE = re.compile("(-?\d+)\.?\d*?( à (-?\d+)\.?\d*?)? (.*)")
RE_CARAC_PA = re.compile("(\d{1,2}) (\d utilisations? par tour)")
RE_CARAC_PO = re.compile("(\d+)( à (\d+))?")
RE_CARAC_CC = re.compile("1/(\d{1,2})( \(\+(\d{1,2})\))?")
RE_CONDITION = re.compile("(.+?) ([><=]) (\d+)")

BLOCK_DESCRIPTION = "Description"
BLOCK_ATTRIBUTES = "Effets"
BLOCK_CARACS = "Caractéristiques"
BLOCK_CONDITIONS = "Conditions"
BLOCK_RECIPE = "Recette"

BASE_URL = "http:/www.dofus.com"
DETAIL_URL_STUFF = "http://www.dofus.com/fr/mmorpg/encyclopedie/equipements/{item_id_name}"
DETAIL_URL_WEAPONS = "http://www.dofus.com/fr/mmorpg/encyclopedie/armes/{item_id_name}"

RECIPE_ELEMENT_SEPARATOR = " ; "

def get_attr(attrs, attr):
    for e in attrs:
        if e[0] == attr:
            return e[1]
    return ""


class MainItemPageParser(HTMLParser):
    def __init__(self, web_cache, history):
        HTMLParser.__init__(self)
        self.web_cache = web_cache
        self.history = history
        
        self.in_table = False
        
    def handle_starttag(self, tag, attrs):
        if tag == "table" and "ak-responsivetable" in get_attr(attrs, "class"):
            self.in_table = True
        
        if self.in_table and tag == "a" and RE_ITEM_ID.match(get_attr(attrs, "href")):
            # item_id_name contains the item id and its formatter name ie: 15495-arc-necrotique
            item_id_name = RE_ITEM_ID.match(get_attr(attrs, "href")).group(1)
            url = DETAIL_URL_STUFF.format(item_id_name=item_id_name)
            log.info(url)
            
            content = self.web_cache.get(url)
            # Extract the id part of the id_name variable
            p = ItemPageParser(re.match("\d+", item_id_name).group(), self.web_cache)
            p.feed(content)
            printItems(p.item)
            if p.has_changed:
                self.history.updated_items.add(p.item)
        
    def handle_endtag(self, tag):
        if self.in_table and tag == "table":
            self.in_table = False

class ItemPageParser(HTMLParser):
    def __init__(self, item_id, web_cache):
        HTMLParser.__init__(self)
        self.reset_vars()
        
        self.item = None
        self.item_id = item_id
        self.web_cache = web_cache
        
    def reset_vars(self):
        self.has_changed = False
        self.current_item_attributes_dump = ""
        self.current_item_conditions_dump = ""
        
        self.get_name = False
        self.in_name = False
        self.get_level = False
        self.get_type = False
        self.in_type = False
        self.content_is_desc = False
        self.get_desc = False
        self.content_is_attributes = False
        self.in_attributes = False
        self.get_attributes = False
        self.content_is_caracs = False
        self.in_caracs = False
        self.get_caracs = False
        self.content_is_conditions = False
        self.in_conditions = False
        self.get_conditions = False
        self.content_is_recipe = False
        self.in_recipe = False
        self.get_recipe_element_number = False
        self.get_recipe_element_name = False
        self.recipe = ""
        self.check_block = False
        
    
    def handle_starttag(self, tag, attrs):
        if tag == "div" and "ak-panel-title" in get_attr(attrs, "class"):
            self.check_block = True
        
        # Item name
        if tag == "div" and "ak-title-container" in get_attr(attrs, "class"):
            self.in_name = True
        if self.in_name and tag == "h1":
            self.get_name = True
            
        # Item type
        if tag == "div" and "ak-encyclo-detail-type" in get_attr(attrs, "class"):
            self.in_type = True
        if self.in_type and tag == "span":
            self.get_type = True
        
        # Item level
        if tag == "div" and "ak-encyclo-detail-level" in get_attr(attrs, "class"):
            self.get_level = True
        
        # Item description
        if self.content_is_desc and tag == "div" and "ak-panel-content" in get_attr(attrs, "class"):
            self.get_desc = True
        
        # Item attributes
        if self.content_is_attributes and tag == "div" and "ak-panel-content" in get_attr(attrs, "class"):
            self.in_attributes = True
        if self.in_attributes and tag == "div" and "ak-title" in get_attr(attrs, "class"):
            self.get_attributes = True
        
        # Item caracteristics
        if self.content_is_caracs and tag == "div" and "ak-panel-content" in get_attr(attrs, "class"):
            self.in_caracs = True
        if self.in_caracs and tag == "div" and "ak-title" in get_attr(attrs, "class"):
            self.get_caracs = True
        
        # Item conditions
        if self.content_is_conditions and tag == "div" and "ak-panel-content" in get_attr(attrs, "class"):
            self.in_conditions = True
        if self.in_conditions and tag == "div" and "ak-title" in get_attr(attrs, "class"):
            self.get_conditions = True
        
        # Item recipe
        if self.content_is_recipe and tag == "div" and "ak-panel-content" in get_attr(attrs, "class"):
            self.in_recipe = True
            
        if self.in_recipe and tag == "div" and "ak-front" in get_attr(attrs, "class"):
            self.get_recipe_element_number = True
        
        if self.in_recipe and tag == "div" and "ak-content" in get_attr(attrs, "class"):
            self.in_recipe_element_name = True
        
        if self.in_recipe_element_name and tag == "span" and "ak-linker" in get_attr(attrs, "class"):
            self.get_recipe_element_name = True
        
        if self.in_recipe and tag == "div" and "ak-social" in get_attr(attrs, "class"):
            self.content_is_recipe = False
            self.in_recipe = False
            
            recipe = self.item.recipe
            if not recipe:
                recipe = Recipe()
            
            recipe.text = self.recipe
            recipe.size = self.recipe.count(" x ")
            recipe.save()
            self.has_changed |= self.item.recipe != recipe
            self.item.recipe = recipe
        
    def handle_data(self, data):
        if self.check_block:
            block = data.strip()
            
            if block == BLOCK_DESCRIPTION:
                self.content_is_desc = True
                
            if block == BLOCK_ATTRIBUTES:
                self.content_is_attributes = True
                
            if block == BLOCK_CARACS:
                self.content_is_attributes = False
                self.in_attributes = False
                self.content_is_caracs = True
                
            if block == BLOCK_CONDITIONS:
                self.content_is_caracs = False
                self.in_caracs = False
                self.content_is_conditions = True
                
            if block == BLOCK_RECIPE:
                self.content_is_recipe = True
        
        
        if self.get_name:
            name = data.strip()
            try:
                self.item = Item.objects.get(name=name)
            except:
                self.item = Item(name=name)
                self.has_changed = True
                
        if self.get_type:
            item_type = ItemType.objects.get(name=data.strip())
            self.has_changed |= self.item.type != item_type
            self.item.type = item_type
    
        if self.get_level:
            match = RE_LEVEL.match(data.strip())
            if match:
                self.has_changed |= self.item.level != int(match.group(1))
                self.item.level = match.group(1)
                
        if self.get_desc:
            self.has_changed |= self.item.description != unicode(data.decode("utf-8"))
            self.item.description = data.strip()
        
        if self.get_attributes:
            match = RE_ATTRIBUTE.match(data)
            if match:
                attr = match.group(4).strip()
                min_value = match.group(1)
                max_value = match.group(3)
                if not max_value:
                    max_value = min_value
                if int(min_value) < 0 and int(max_value) > 0:
                    max_value = "-"+max_value
                
                # if not Attribute.objects.get_if_exist(name=attr):
                    # log.debug(match.groups())
                    # raise Exception("Weird attribute:" + attr + " on " + self.item.name)
                
                attr, _created = Attribute.objects.get_or_create(name=attr)
                
                AttributeValue.objects.get_or_create(item=self.item, attribute=attr, min_value=int(min_value), max_value=int(max_value))
        
        
        if self.get_caracs:
            pa = RE_CARAC_PA.match(data)
            po = RE_CARAC_PO.match(data)
            cc = RE_CARAC_CC.match(data)
            
            if pa:
                self.has_changed |= self.item.cost != int(pa.group(1))
                self.item.cost = int(pa.group(1))
                
            if po:
                self.has_changed |= self.item.range_min != int(po.group(1)) and self.item.range_max != int(po.group(3))
                self.item.range_min = int(po.group(1))
                self.item.range_max = int(po.group(3))
            
            if cc:
                self.has_changed |= self.item.crit_chance != int(cc.group(1))
                self.item.crit_chance = int(cc.group(1))
                if cc.group(3):
                    self.has_changed |= self.item.crit_damage != int(cc.group(3))
                    self.item.crit_damage = int(cc.group(3))
        
        if self.get_conditions:
            match = RE_CONDITION.match(data)
            if match:
                attr, equality, value = match.groups()
                attr, _created = Attribute.objects.get_or_create(name=attr.strip())
                
                AttributeCondition.objects.get_or_create(item=self.item, attribute=attr, equality=equality.strip(), required_value=value)
         
        if self.get_recipe_element_number:
            if self.recipe:
                self.recipe += RECIPE_ELEMENT_SEPARATOR
            self.recipe += data.strip()
        
        if self.get_recipe_element_name:
            self.recipe += data.strip()
        
    def handle_endtag(self, tag):
        if self.check_block and tag == "div":
            self.check_block = False
        
        if self.get_name and tag == "h1":
            self.in_name = False
            self.get_name = False
        
        if self.get_type and tag == "span":
            self.in_type = False
            self.get_type = False
            
        if self.get_level and tag == "div":
            self.get_level = False
        
        if self.get_desc and tag == "div":
            self.get_desc = False
            self.content_is_desc = False
            
        if self.get_attributes and tag == "div":
            self.get_attributes = False
        
        if self.get_caracs and tag == "div":
            self.get_caracs = False
        
        if self.get_conditions and tag == "div":
            self.get_conditions = False
            self.in_conditions = False
            self.content_is_conditions = False
        
        if self.get_recipe_element_number and tag == "div":
            self.get_recipe_element_number = False
        
        if self.get_recipe_element_name and tag == "span":
            self.in_recipe_element_name = False
            self.get_recipe_element_name = False
