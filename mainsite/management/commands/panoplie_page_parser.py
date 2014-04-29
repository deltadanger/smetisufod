# -*- coding: utf-8 -*-
import re, logging

from HTMLParser import HTMLParser

from mainsite.models import I18nString, Panoplie, PanoplieAttribute, Attribute, Item


BASE_URL = "http://www.dofus.com"


RE_NO_ITEMS = re.compile("(\d) Objets")
RE_ATTRIBUTE = re.compile("(\d+) (.*)")



log = logging.getLogger(__name__)


def get_attr(attrs, attr):
    for e in attrs:
        if e[0] == attr:
            return e[1]
    return ""

class MainPanopliePageParser(HTMLParser):
    def __init__(self, web_cache):
        HTMLParser.__init__(self)
        self.web_cache = web_cache
        
        self.in_menu = False
        
    def handle_starttag(self, tag, attrs):
        if tag == "div" and "sous_menu_encyclo" in get_attr(attrs, "class"):
            self.in_menu = True
        
        if self.in_menu and tag == "a" and "/fr/mmorpg-jeux/panoplies/" in get_attr(attrs, "href"):
            url = BASE_URL + get_attr(attrs, "href")
            log.debug(url)
            
            resp = self.web_cache.get(url)
            PanopliePageParser().feed(resp.read())
        
    def handle_endtag(self, tag):
        if self.in_menu and tag == "div":
            self.in_menu = False


class PanopliePageParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        
        self.panoplie = None
        self.current_no_item = 0
        
        self.in_name = False
        self.get_name = False
        self.in_bonuses = False
        self.get_bonuses = False
        self.get_item = False
        
        
    def handle_starttag(self, tag, attrs):
        if tag == "div" and "content_panos" in get_attr(attrs, "class"):
            self.in_name = True
        
        if self.in_name and tag == "h2":
            self.get_name = True
        
        if self.in_name and tag == "span":
            self.get_name = False
            self.in_name = False
        
        if self.in_bonuses and tag == "ul":
            self.get_bonuses = True
        
        if tag == "h2" and "title_element" in get_attr(attrs, "class"):
            self.get_item = True
        
    def handle_data(self, data):
        if self.get_name:
            name, created = I18nString.objects.get_or_create(fr_fr=data)
            self.panoplie, created = Panoplie.objects.get_or_create(name=name)
            log.debug("Name: " + data+" ("+str(created)+")")
        
        if "Bonus de la panoplie" in data:
            self.in_bonuses = True
        
        if self.get_bonuses:
            no_item_match = RE_NO_ITEMS.match(data)
            attribute_match = RE_ATTRIBUTE.match(data)
            
            if no_item_match:
                self.current_no_item = int(no_item_match.group(1))
                
            elif attribute_match:
                if not self.current_no_item:
                    raise Exception("Parsing mismatch, 'current_no_of_item' should be set. " + self.panoplie.name.fr_fr)
                value = attribute_match.group(1)
                name = attribute_match.group(2)
                name, created = I18nString.objects.get_or_create(fr_fr=name)
                attribute, created = Attribute.objects.get_or_create(name=name)
                
                log.debug(str(value) + " " + attribute.name.fr_fr + " for " + str(self.current_no_item) + " objects"+" ("+str(created)+")")
                PanoplieAttribute.objects.get_or_create(panoplie=self.panoplie, attribute=attribute, value=value, no_of_items=self.current_no_item)
        
        if self.get_item:
            name = I18nString.objects.get(fr_fr=data)
            item = Item.objects.get(name=name)
            item.panoplie = self.panoplie
            item.save()
            log.debug("Item " + unicode(name) + " belongs to " + unicode(self.panoplie.name))
        
    def handle_endtag(self, tag):
        if self.get_item and tag == "h2":
            self.get_item = False
        
        if self.get_bonuses and tag == "ul":
            self.get_bonuses = False
            self.in_bonuses = False

