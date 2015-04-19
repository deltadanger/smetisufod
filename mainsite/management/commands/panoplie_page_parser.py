# -*- coding: utf-8 -*-
import re, logging

from HTMLParser import HTMLParser

from mainsite.models import Panoplie, PanoplieAttribute, Attribute, Item

BASE_URL = "http://www.dofus.com"

RE_ITEM_ID = re.compile("/fr/mmorpg/encyclopedie/.+?/(\d+)-")
RE_NO_ITEMS = re.compile(".*set-bonus-(\d)")
RE_ATTRIBUTE = re.compile("(\d+) (.*)")

log = logging.getLogger(__name__)

def get_attr(attrs, attr):
    for e in attrs:
        if e[0] == attr:
            return e[1]
    return ""

class MainPanopliePageParser(HTMLParser):
    def __init__(self, web_cache, history):
        HTMLParser.__init__(self)
        self.web_cache = web_cache
        self.history = history
        
        self.in_table = False
        self.in_row = False
        self.in_link_container = False
        
    def handle_starttag(self, tag, attrs):
        if tag == "tbody":
            self.in_table = True
        
        if self.in_table and tag == "tr":
            self.in_row = True
        
        if self.in_row and tag == "span" and "ak-linker" in get_attr(attrs, "class"):
            self.in_link_container = True
        
        if self.in_link_container and tag == "a" and "/fr/mmorpg/encyclopedie/panoplies" in get_attr(attrs, "href"):
            url = BASE_URL + get_attr(attrs, "href")
            log.debug("\n")
            content = self.web_cache.get(url)
            p = PanopliePageParser()
            try:
                p.feed(content)
            except InvalidPanoplie as e:
                log.warning(e.message)
            else:
                if p.has_changed:
                    self.history.updated_panos.add(p.panoplie)
                    self.history.updated_items.add(*p.changed_items)
        
    def handle_endtag(self, tag):
        if self.in_table and tag == "tbody":
            self.in_table = False
            
        if self.in_row and tag == "tr":
            self.in_row = False
        
        if self.in_link_container and tag == "span":
            self.in_link_container = False


class PanopliePageParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        
        self.panoplie = None
        self.current_no_item = 0
        self.has_changed = False
        self.attributes_dump = ""
        self.changed_items = []
        
        self.in_name = False
        self.get_name = False
        self.in_item = False
        self.in_bonuses = False
        self.get_bonuses = False
        
        
    def handle_starttag(self, tag, attrs):
        if tag == "div" and "ak-title-container" in get_attr(attrs, "class"):
            self.in_name = True
        
        if self.in_name and tag == "h1":
            self.get_name = True
        
        if tag == "div" and "ak-item-list-preview" in get_attr(attrs, "class"):
            self.in_item = True
            
        if self.in_item and tag == "a":
#             log.debug(RE_ITEM_ID.match(get_attr(attrs, "href")))
            item_id = RE_ITEM_ID.match(get_attr(attrs, "href")).group(1)
            try:
                item = Item.objects.get(original_id=item_id)
            except:
                self.panoplie.delete()
                raise InvalidPanoplie("Item " + item_id + " does not exist, panoplie " + self.panoplie.name + " has been removed.")
            else:
                if item.panoplie != self.panoplie:
                    self.has_changed = True
                    self.changed_items.append(item)
                    
                    item.panoplie = self.panoplie
                    item.save()
                # log.debug("Item " + name + " belongs to " + self.panoplie.name)
        
        if tag == "div" and "set-bonus-list" in get_attr(attrs, "class"):
            self.in_bonuses = True
            self.current_no_item = RE_NO_ITEMS.match(get_attr(attrs, "class")).group(1)
        
        if self.in_bonuses and tag == "div" and "ak-title" in get_attr(attrs, "class"):
            self.get_bonuses = True
        
        if self.get_bonuses and tag == "div" and "ak-nocontentpadding" in get_attr(attrs, "class"):
            self.get_bonuses = False
            self.in_bonuses = False
            
            self.has_changed |= self.attributes_dump != str(self.panoplie.panoplieattribute_set.all())
        
    def handle_data(self, data):
        if self.get_name:
            pano_name = data.strip()
            if pano_name:
                self.panoplie, created = Panoplie.objects.get_or_create(name=pano_name)
                log.debug("Name: " + pano_name +" ("+str(created)+")")
                self.has_changed |= created
                
                self.attributes_dump = str(self.panoplie.panoplieattribute_set.all())
                self.panoplie.attributes.clear()
        
        if self.get_bonuses:
            attribute_match = RE_ATTRIBUTE.match(data.strip())
            if attribute_match:
                if not self.current_no_item:
                    self.panoplie.delete()
                    raise InvalidPanoplie("Parsing mismatch, 'current_no_of_item' should be set, panoplie " + self.panoplie.name + " has been removed.")
                value = attribute_match.group(1)
                name = attribute_match.group(2)
                attribute, _created = Attribute.objects.get_or_create(name=name)
                
                log.debug(str(value) + ":" + attribute.name + " for " + str(self.current_no_item) + " objects"+" ("+str(_created)+")")
                PanoplieAttribute.objects.create(panoplie=self.panoplie, attribute=attribute, value=value, no_of_items=self.current_no_item)
        
    def handle_endtag(self, tag):
        if self.in_name and tag == "div":
            self.in_name = False
            
        if self.get_name and tag == "h1":
            self.get_name = False
        
        if self.in_item and tag == "div":
            self.in_item = False
        

class InvalidPanoplie(Exception):
    pass