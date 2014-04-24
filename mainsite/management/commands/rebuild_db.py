# -*- coding: utf-8 -*- 
import urllib2, unicodedata, string, re
from HTMLParser import HTMLParser

from django.core.management.base import BaseCommand, CommandError
from mainsite.models import I18nString, Item, ItemType, ItemCategory, Attribute, AttributeValues, AttributeCondition

PROXY = "http://jacoelt:8*ziydwys@crlwsgateway_cluster.salmat.com.au:8080"
PROXY_LIST = {"http":PROXY, "https":PROXY}

BASE_URL = "http://www.dofus.com/fr/mmorpg-jeux/objets/2-objets/10-ceinture"


RE_LEVEL = re.compile("Level (\d+)")
RE_ATTRIBUTE = re.compile("(-?\d+)( à (-?\d+))? (.*)".decode("utf-8"))

COOKIES = "LANG=fr; SID=E1E002989B2E28B1544466C1DFE80000"


class Command(BaseCommand):
    help = 'Update or rebuild the items database'
    
    def handle(self, *args, **options):
        proxy = urllib2.ProxyHandler(PROXY_LIST)
        opener = urllib2.build_opener(proxy)
        opener.addheaders.append(('Cookie', COOKIES))
        resp = opener.open(BASE_URL)
        
        p = ItemPageParser()
        p.feed(resp.read())
        
        for item in p.data:
            printItem(item)
            

def printItem(item):
    print item.name
    for a in item.attributes.all():
        values = a.attributevalues_set.get(item=item)
        print a.name, ":" + str(values.min_value) + "-" + str(values.max_value)
    print "\n"

def get_attr(attrs, attr):
    for e in attrs:
        if e[0] == attr:
            return e[1]
    return ""

class ItemPageParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.reset_vars()
        
        self.data = []
        self.item = None
        
    def reset_vars(self):
        self.get_name = False
        self.get_level = False
        self.in_desc = False
        self.get_desc = False
        self.in_attributes = False
        self.in_attributes_left = False
        self.get_attributes = False
        self.in_attributes_right = False
        self.in_conditions = False
        self.get_conditions = False
        
    
    def handle_starttag(self, tag, attrs):
        if tag == "div" and "middle_content" in get_attr(attrs, "class"):
            if self.item:
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
            self.in_attributes = True
            
        if self.in_attributes and tag == "div" and "element_carac_left" in get_attr(attrs, "class"):
            self.in_attributes_left = True
        
        if self.in_attributes and tag == "ul":
            self.get_attributes = True
        
            
        if self.in_attributes and tag == "div" and "element_carac_right" in get_attr(attrs, "class"):
            self.in_attributes_left = False
            self.get_attributes = False
            self.in_attributes_right = True
        
        if self.in_conditions and tag == "ul":
            self.get_conditions = True
        
        
    def handle_data(self, data):
        if self.get_name:
            name, created = I18nString.objects.get_or_create(fr_fr=unicode(data))
            self.item, created = Item.objects.get_or_create(name=name)
        
        if self.get_level:
            match = RE_LEVEL.match(data)
            if match:
                self.item.level = match.group(1)
        
        if self.get_desc:
            self.item.description, created = I18nString.objects.get_or_create(fr_fr=unicode(data))
        
        if self.get_attributes:
            match = RE_ATTRIBUTE.match(data)
            if match:
                name, created = I18nString.objects.get_or_create(fr_fr=unicode(match.group(4)))
                min = match.group(1)
                max = match.group(3)
                if not max:
                    max = min
                
                attr, created = Attribute.objects.get_or_create(name=name)
                try:
                    AttributeValues.objects.get(item=self.item, attribute=attr, min_value=int(min), max_value=int(max))
                except:
                    AttributeValues.objects.create(item=self.item, attribute=attr, min_value=int(min), max_value=int(max))
        
        if self.in_attributes_right and "Conditions :" in data:
            self.in_conditions = True
        
        
    def handle_endtag(self, tag):
        if self.get_conditions and tag == "ul":
            self.get_conditions = False
            self.in_conditions = False
        
        if self.get_attributes and tag == "ul":
            self.get_attributes = False
            self.in_attributes_left = False
            self.in_attributes = False
            
        if self.get_desc and tag == "span":
            self.get_desc = False
            self.in_desc = False
        
        if self.get_name and tag == "h2":
            self.get_name = False
        
        if self.get_level and tag == "span":
            self.get_level = False
        
    

if __name__ == "__main__":
    run()
