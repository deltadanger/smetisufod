# -*- coding: utf-8 -*- 
import urllib2, unicodedata, string, re
from HTMLParser import HTMLParser

# from models import Item, I18nString
# from mainsite.models import I18nString, Item, ItemType, ItemCategory, Attribute, AttributeValues, AttributeCondition, Recipe

PROXY = "http://jacoelt:8*ziydwys@crlwsgateway_cluster.salmat.com.au:8080"
PROXY_LIST = {"http":PROXY, "https":PROXY}

BASE_URL = "http://www.dofus.com/fr/mmorpg-jeux/objets/2-objets/10-ceinture"


LEVEL_RE = re.compile("Level (\d+)")
ATTRIBUTE_RE = re.compile("(-?\d+)( à (-?\d+))? (.*)".decode("utf-8"))

COOKIES = "LANG=fr; SID=E1E002989B2E28B1544466C1DFE80000"

def run():
    proxy = urllib2.ProxyHandler(PROXY_LIST)
    opener = urllib2.build_opener(proxy)
    opener.addheaders.append(('Cookie', COOKIES))
    resp = opener.open(BASE_URL)
    
    p = ItemPageParser()
    p.feed(resp.read().decode("utf-8"))
    
    for item in p.data:
        printItem(item)

def printItem(item):
    print item.name
    for a in item.attributes:
        print a
    print "\n"

class Item():
    name = ""
    description = ""
    level = -1
    attributes = []
    craft = []
    condition = []
    cost = -1
    range = -1
    critical = -1
    failure = -1

class Attribute():
    def __init__(self, min=-1, max=-1, name=""):
        self.min = min
        self.max = max
        self.name = name
    
    def __repr__(self):
        if self.min == self.max:
            return self.name + ":" + str(self.min)
        return self.name + ":" + str(self.min) + "-" + str(self.max)

def get_attr(attrs, attr):
    for e in attrs:
        if e[0] == attr:
            return e[1]
    return ""

class ItemPageParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        
        self.get_name = False
        self.get_level = False
        self.in_desc = False
        self.get_desc = False
        self.in_attributes = False
        self.get_attributes = False
        
        self.data = []
        self.item = None
        
    
    def handle_starttag(self, tag, attrs):
        if tag == "div" and get_attr(attrs, "class") == "middle_content":
            if self.item:
                self.data.append(self.item)
            self.item = Item()
            
        
        if tag == "h2" and get_attr(attrs, "class") == "title_element":
            self.get_name = True
        
        if tag == "span" and get_attr(attrs, "class") == "level_element":
            self.get_level = True
        
        
        if tag == "div" and get_attr(attrs, "class") == "desc":
            self.in_desc = True
        
        if self.in_desc and tag == "span":
            self.get_desc = True
        
        
        if tag == "div" and get_attr(attrs, "class") == "element_carac_left":
            self.in_attributes = True
        
        if self.in_attributes and tag == "ul":
            self.get_attributes = True
        
        
    def handle_data(self, data):
        if self.get_name:
            # self.item.name = I18nString(fr_fr=data.encode("utf-8"))
            self.item.name = data.encode("utf-8")
        
        if self.get_level:
            match = LEVEL_RE.match(data)
            if match:
                self.item.level = match.group(1)
        
        if self.get_desc:
            # self.item.description = I18nString(fr_fr=data.encode("utf-8"))
            self.item.description = data.encode("utf-8")
        
        if self.get_attributes:
            match = ATTRIBUTE_RE.match(data)
            if match:
                if match.group(3):
                    attr = Attribute(int(match.group(1)), int(match.group(3)), match.group(4).encode("utf-8"))
                else:
                    attr = Attribute(int(match.group(1)), int(match.group(1)), match.group(4).encode("utf-8"))
                
                self.item.attributes.append(attr)
        
    def handle_endtag(self, tag):
        if self.get_attributes and tag == "ul":
            self.get_attributes = False
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
