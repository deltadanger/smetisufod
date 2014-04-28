
import urllib2

from django.core.management.base import BaseCommand, CommandError

from item_page_parser import ItemPageParser


PROXY = "http://jacoelt:8*ziydwys@crlwsgateway_cluster.salmat.com.au:8080"
PROXY_LIST = {"http":PROXY, "https":PROXY}

# BASE_URL = "http://www.dofus.com/fr/mmorpg-jeux/objets/2-objets/10-ceinture"
BASE_URL = "http://www.dofus.com/fr/mmorpg-jeux/objets/"

CATEGORIES = [
    "Arme",
    "Equipement",
    "Familier",
    "Monture",
    "Ressource",
    "Consomable",
]

JOBS = [
    "",
]

CATEGORY_MAPPING = [
    {"url": "2-objets/1-amulette", "category": "Equipement", "type": "Amulette", "job": "Bijouter"},
    {"url": "2-objets/9-anneau", "category": "Equipement", "type": "Anneau", "job": "Bijouter"},
    {"url": "2-objets/16-chapeau", "category": "Equipement", "type": "Chapeau", "job": "Tailleur"},
    {"url": "2-objets/17-cape", "category": "Equipement", "type": "Cape", "job": "Tailleur"},
    {"url": "2-objets/81-sac-dos", "category": "Equipement", "type": "Sac a Dos", "job": "Tailleur"},
    {"url": "2-objets/10-ceinture", "category": "Equipement", "type": "Ceinture", "job": "Cordonnier"},
    {"url": "2-objets/11-bottes", "category": "Equipement", "type": "Bottes", "job": "Cordonnier"},
    {"url": "2-objets/82-bouclier", "category": "Equipement", "type": "Bouclier", "job": "Forgeur de Boucliers"},
    {"url": "1-armes/2-arc", "category": "Arme", "type": "Arc", "job": "Sculpteur d'Arcs"},
    {"url": "1-armes/3-baguette", "category": "Arme", "type": "Baguette", "job": "Sculpteur de Baguettes"},
    {"url": "1-armes/4-baton", "category": "Arme", "type": "Baton", "job": "Sculpteur de Baton"},
    {"url": "1-armes/5-dague", "category": "Arme", "type": "Dague", "job": "Forgeur de Dagues"},
    {"url": "1-armes/6-epee", "category": "Arme", "type": "Epée", "job": "Forgeur d'Epées"},
    {"url": "1-armes/7-marteau", "category": "Arme", "type": "Marteau", "job": "Forgeur de Marteaux"},
    {"url": "1-armes/8-pelle", "category": "Arme", "type": "Pelle", "job": "Forgeur de Pelle"},
    {"url": "1-armes/19-hache", "category": "Arme", "type": "Hache", "job": "Forgeur de Haches"},
    {"url": "1-armes/20-outil", "category": "Arme", "type": "Outil", "job": None},
    {"url": "4-ressources/15-ressources-diverses", "category": "Ressource", "type": "Ressource", "job": None},
    {"url": "4-ressources/26-potion-forgemagie", "category": "Ressource", "type": "", "job": None},
    {"url": "4-ressources/34-cereale", "category": "Ressource", "type": "", "job": None},
    {"url": "4-ressources/35-fleur", "category": "Ressource", "type": "", "job": None},
    {"url": "4-ressources/36-plante", "category": "Ressource", "type": "", "job": None},
    {"url": "4-ressources/38-bois", "category": "Ressource", "type": "", "job": None},
    {"url": "4-ressources/39-minerai", "category": "Ressource", "type": "", "job": None},
    {"url": "4-ressources/40-aliage", "category": "Ressource", "type": "", "job": None},
    {"url": "4-ressources/41-poisson", "category": "Ressource", "type": "", "job": None},
    {"url": "4-ressources/46-fruit", "category": "Ressource", "type": "", "job": None},
    {"url": "4-ressources/47-os", "category": "Ressource", "type": "", "job": None},
    {"url": "4-ressources/", "category": "Ressource", "type": "", "job": None},
    {"url": "", "category": "", "type": "", "job": None},
    {"url": "", "category": "", "type": "", "job": None},
    {"url": "", "category": "", "type": "", "job": None},
    {"url": "", "category": "", "type": "", "job": None},
    {"url": "", "category": "", "type": "", "job": None},
    {"url": "", "category": "", "type": "", "job": None},
    {"url": "", "category": "", "type": "", "job": None},
    {"url": "", "category": "", "type": "", "job": None},
    {"url": "", "category": "", "type": "", "job": None},
    {"url": "", "category": "", "type": "", "job": None},
    {"url": "", "category": "", "type": "", "job": None},
    {"url": "", "category": "", "type": "", "job": None},
    {"url": "", "category": "", "type": "", "job": None},
]

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
    print item.name.fr_fr
    for a in item.attributes.all():
        attribute = a.attributevalues_set.get(item=item)
        print a.name.fr_fr, ":" + str(attribute.min_value) + "-" + str(attribute.max_value)
    
    print "\nConditions"
    for c in item.conditions.all():
        condition = c.attributecondition_set.get(item=item)
        print c.name.fr_fr, condition.equality, condition.required_value
    
    print "\nCaracs"
    print str(item.cost) + " PA ; " + str(item.range) + " PO ; CC 1/" + str(item.crit_chance) + " (+" + str(item.crit_damage) + ") ; EC 1/" + str(item.failure)
    
    print "\nCraft"
    craft = []
    if item.has_valid_recipe:
        for i in item.craft.all():
            recipe = i.recipe_element_set.get(recipe_item=item)
            craft.append(str(recipe.quantity) + " x " + recipe.recipe_element.name.fr_fr)
        print ",".join(craft)
        
    else:
        print "Invalid recipe"
    print "\n"


    

if __name__ == "__main__":
    run()
