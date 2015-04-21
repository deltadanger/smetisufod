# -*- coding: utf-8 -*-
from HTMLParser import HTMLParser
import re, logging

from mainsite.models import Item, Attribute, AttributeValue, AttributeCondition, Recipe, \
    ItemType
from pictures import upload_image_file, is_image_available

log = logging.getLogger(__name__)

RE_ITEM_ID = re.compile("/fr/mmorpg/encyclopedie/[a-z]+/(.*)")

RE_LEVEL = re.compile("Niveau : (\d+)")
RE_ATTRIBUTE = re.compile("(-?\d+)\.?\d*?( à (-?\d+)\.?\d*?)? (.*)")
RE_CARAC_PA = re.compile("(\d{1,2}) \(\d utilisations? par tour\)")
RE_CARAC_PO = re.compile("(\d+)( à (\d+))?$")
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
        self.in_row = False
        self.in_link = False
        
    def handle_starttag(self, tag, attrs):
        if tag == "table" and "ak-responsivetable" in get_attr(attrs, "class"):
            self.in_table = True
        
        if self.in_table and tag == "tr":
            self.in_row = True
        
        if self.in_row and tag == "span" and "ak-linker" in get_attr(attrs, "class"):
            self.in_link = True
        
        if self.in_link and tag == "a" and "fr/mmorpg/encyclopedie/" in get_attr(attrs, "href"):
            # item_id_name contains the item id and its formatter name ie: 15495-arc-necrotique
            item_id_name = RE_ITEM_ID.match(get_attr(attrs, "href")).group(1)
            url = DETAIL_URL_STUFF.format(item_id_name=item_id_name)
            
            content = self.web_cache.get(url)
            # Extract the id part of the id_name variable
            p = ItemPageParser(re.match("\d+", item_id_name).group())
            p.feed(content)
            if p.has_changed:
                p.item.save()
                self.history.updated_items.add(p.item)
#                 print p.item.full_str
            
            self.in_row = False
            self.in_link = False
        
    def handle_endtag(self, tag):
        if self.in_table and tag == "table":
            self.in_table = False

class ItemPageParser(HTMLParser):
    def __init__(self, item_id):
        HTMLParser.__init__(self)
        self.reset_vars()
        
        self.item = None
        self.item_id = item_id
        
    def reset_vars(self):
        self.has_changed = False
        self.current_item_attributes_dump = ""
        self.current_item_conditions_dump = ""
        
        self.in_name = False
        self.get_name = False
        self.in_image = False
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
        self.in_recipe_element_name = False
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
        
        # Item image
        if tag == "div" and "ak-encyclo-detail-illu" in get_attr(attrs, "class"):
            self.in_image = True
        if self.in_image and tag == "img":
            # TODO: check if image is different
            url = get_attr(attrs, "src")
            new_image_name = url.split("/")[-1]
            current_image_name = self.item.image.split("/")[-1] if self.item.image else None
            if new_image_name != current_image_name:
                image = upload_image_file(url)
                self.has_changed = True
                self.item.image = image
        
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
        if self.in_attributes and tag == "div" and "ak-panel " in get_attr(attrs, "class"):
            self.content_is_attributes = False
            self.in_attributes = False
        
        # Item caracteristics
        if self.content_is_caracs and tag == "div" and "ak-panel-content" in get_attr(attrs, "class"):
            self.in_caracs = True
        if self.in_caracs and tag == "div" and "ak-title" in get_attr(attrs, "class"):
            self.get_caracs = True
        if self.in_caracs and tag == "div" and "ak-panel " in get_attr(attrs, "class"):
            self.content_is_caracs = False
            self.in_caracs = False
        
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
                self.content_is_caracs = True
                
            if block == BLOCK_CONDITIONS:
                self.content_is_conditions = True
                
            if block == BLOCK_RECIPE:
                self.content_is_recipe = True
        
        if self.get_name:
            name = data.strip()
            if name:
                self.item, _created = Item.objects.get_or_create(name=name)
                self.item.attributes.clear()
                
                self.has_changed |= self.item.original_id != self.item_id
                self.item.original_id = self.item_id
                
        if self.get_type:
            try:
                item_type = ItemType.objects.get(name=data.strip())
                self.has_changed |= self.item.type != item_type
                self.item.type = item_type
            except ItemType.DoesNotExist:
                log.debug("Could not find item type '{}'".format(data.strip()))
                raise
    
        if self.get_level:
            match = RE_LEVEL.match(data.strip())
            if match:
                self.has_changed |= self.item.level != int(match.group(1))
                self.item.level = match.group(1)
                
        if self.get_desc:
            self.has_changed |= self.item.description != unicode(data.decode("utf-8"))
            self.item.description = data.strip()
        
        if self.get_attributes:
            match = RE_ATTRIBUTE.match(data.strip())
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
                
                AttributeValue.objects.create(item=self.item, attribute=attr, min_value=int(min_value), max_value=int(max_value))
        
        
        if self.get_caracs:
#             log.debug("get caracs")
#             log.debug("|" + data.strip() + "|")
            pa = RE_CARAC_PA.match(data.strip())
            po = RE_CARAC_PO.match(data.strip())
            cc = RE_CARAC_CC.match(data.strip())
            
            if pa:
#                 log.debug(pa.groups())
                self.has_changed |= self.item.cost != int(pa.group(1))
                self.item.cost = int(pa.group(1))
                
            if po:
#                 log.debug(po.groups())
                min_range = po.group(1)
                max_range = po.group(3)
                if not max_range:
                    max_range = min_range
                self.has_changed |= self.item.range_min != int(min_range) and self.item.range_max != int(max_range)
                self.item.range_min = int(min_range)
                self.item.range_max = int(max_range)
            
            if cc:
                self.has_changed |= self.item.crit_chance != int(cc.group(1))
                self.item.crit_chance = int(cc.group(1))
                if cc.group(3):
                    self.has_changed |= self.item.crit_damage != int(cc.group(3))
                    self.item.crit_damage = int(cc.group(3))
        
        if self.get_conditions:
#             log.debug("get conditions")
#             log.debug("|" + data.strip() + "|")
            match = RE_CONDITION.match(data.strip())
            if match:
                attr, equality, value = match.groups()
                attr, _created = Attribute.objects.get_or_create(name=attr.strip())
                
                AttributeCondition.objects.get_or_create(item=self.item, attribute=attr, equality=equality.strip(), required_value=value)
         
        if self.get_recipe_element_number:
            if self.recipe:
                self.recipe += RECIPE_ELEMENT_SEPARATOR
            self.recipe += data.strip()
        
        if self.get_recipe_element_name:
            self.recipe += " " + data.strip()
        
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
