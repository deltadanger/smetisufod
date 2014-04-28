# -*- coding: utf-8 -*-
import urllib2

from django.core.management.base import BaseCommand, CommandError

from item_page_parser import ItemPageParser

from mainsite.models import Item, ItemCategory, ItemType, Job 


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
    "Bijouter",
    "Tailleur",
    "Cordonnier",
    "Forgeur de Boucliers",
    "Sculpteur d'Arcs",
    "Sculpteur de Baguettes",
    "Sculpteur de Baton",
    "Forgeur de Dagues",
    "Forgeur d'Epées",
    "Forgeur de Marteaux",
    "Forgeur de Pelle",
    "Forgeur de Haches",
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
    
    {"url": "4-ressources/15-ressources-diverses",  "category": "Ressource", "type": "Ressource", "job": None},
    {"url": "4-ressources/26-potion-forgemagie",    "category": "Ressource", "type": "Potion de Forgemagie", "job": None},
    {"url": "4-ressources/34-cereale",              "category": "Ressource", "type": "Cérérale", "job": None},
    {"url": "4-ressources/35-fleur",                "category": "Ressource", "type": "Fleur", "job": None},
    {"url": "4-ressources/36-plante",               "category": "Ressource", "type": "Plante", "job": None},
    {"url": "4-ressources/38-bois",                 "category": "Ressource", "type": "Bois", "job": None},
    {"url": "4-ressources/39-minerai",              "category": "Ressource", "type": "Minerai", "job": None},
    {"url": "4-ressources/40-aliage",               "category": "Ressource", "type": "Aliage", "job": None},
    {"url": "4-ressources/41-poisson",              "category": "Ressource", "type": "Poisson", "job": None},
    {"url": "4-ressources/46-fruit",                "category": "Ressource", "type": "Fruit", "job": None},
    {"url": "4-ressources/47-os",                   "category": "Ressource", "type": "Os", "job": None},
    {"url": "4-ressources/48-poudre",               "category": "Ressource", "type": "Poudre", "job": None},
    {"url": "4-ressources/50-pierre-precieuse",     "category": "Ressource", "type": "Pierre Précieuse", "job": None},
    {"url": "4-ressources/51-pierre-brute",         "category": "Ressource", "type": "Pierre Brute", "job": None},
    {"url": "4-ressources/52-farine",               "category": "Ressource", "type": "Farine", "job": None},
    {"url": "4-ressources/53-plume",                "category": "Ressource", "type": "Plume", "job": None},
    {"url": "4-ressources/54-poil",                 "category": "Ressource", "type": "Poil", "job": None},
    {"url": "4-ressources/55-etoffe",               "category": "Ressource", "type": "Etoffe", "job": None},
    {"url": "4-ressources/56-cuir",                 "category": "Ressource", "type": "Cuir", "job": None},
    {"url": "4-ressources/57-laine",                "category": "Ressource", "type": "Laine", "job": None},
    {"url": "4-ressources/58-graine",               "category": "Ressource", "type": "Graine", "job": None},
    {"url": "4-ressources/59-peau",                 "category": "Ressource", "type": "Peau", "job": None},
    {"url": "4-ressources/60-huile",                "category": "Ressource", "type": "Huile", "job": None},
    {"url": "4-ressources/61-peluche",              "category": "Ressource", "type": "Peluche", "job": None},
    {"url": "4-ressources/62-poisson-vide",         "category": "Ressource", "type": "Poisson Vidé", "job": None},
    {"url": "4-ressources/63-viande",               "category": "Ressource", "type": "Viande", "job": None},
    {"url": "4-ressources/64-viande-conservee",     "category": "Ressource", "type": "Viande Conservée", "job": None},
    {"url": "4-ressources/65-queue",                "category": "Ressource", "type": "Queue", "job": None},
    {"url": "4-ressources/66-metaria",              "category": "Ressource", "type": "Metaria", "job": None},
    {"url": "4-ressources/68-legume",               "category": "Ressource", "type": "Legume", "job": None},
    {"url": "4-ressources/70-teinture",             "category": "Ressource", "type": "Teinture", "job": None},
    {"url": "4-ressources/71-materiel-alchimie",    "category": "Ressource", "type": "Matériel d'Alchimie", "job": None},
    {"url": "4-ressources/78-rune-forgemagie",      "category": "Ressource", "type": "Rune de Forgemagie", "job": None},
    {"url": "4-ressources/84-clef",                 "category": "Ressource", "type": "Clef", "job": None},
    {"url": "4-ressources/90-fantome-familier",     "category": "Ressource", "type": "Fantome de Familier", "job": None},
    {"url": "4-ressources/95-planche",              "category": "Ressource", "type": "Planche", "job": None},
    {"url": "4-ressources/96-ecorce",               "category": "Ressource", "type": "Ecorce", "job": None},
    {"url": "4-ressources/98-racine",               "category": "Ressource", "type": "Racine", "job": None},
    {"url": "4-ressources/119-champignon",          "category": "Ressource", "type": "Champignon", "job": None},
    {"url": "4-ressources/152-galet",               "category": "Ressource", "type": "Galet", "job": None},
    {"url": "4-ressources/153-nowel",               "category": "Ressource", "type": "Nowel", "job": None},
    {"url": "4-ressources/167-essence-gardien-donjon", "category": "Ressource", "type": "Essence de Gardien de Donjon", "job": None},
    
    {"url": "5-familiers/18-familier", "category": "Familier", "type": "Familier", "job": None},
    {"url": "5-familiers/121-montilier", "category": "Familier", "type": "Montilier", "job": None},
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
        
        
        
        printItems()



def build_categories():
    for c in CATEGORIES:
        name, created = I18nString.objects.get_or_create(fr_fr=c)
        ItemCategory.objects.get_or_create(name=name)
    
def build_jobs():
    for j in JOBS:
        name, created = I18nString.objects.get_or_create(fr_fr=j)
        ItemCategory.objects.get_or_create(name=name)
    


def printItem():
    for item in Item.objects.all():
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
