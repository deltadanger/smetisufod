# -*- coding: utf-8 -*-
import urllib2, logging
from optparse import make_option

from django.core.management.base import BaseCommand
from django.utils import timezone

from web_cache import WebCache

from item_page_parser import MainItemPageParser
from panoplie_page_parser import MainPanopliePageParser

from mainsite.models import Item, ItemCategory, ItemType, Job, UpdateHistory

from smetisufod.settings import DOFUS_COOKIES

log = logging.getLogger(__name__)

STUFF_URL = "http://www.dofus.com/fr/mmorpg/encyclopedie/equipements?size=99999"
WEAPONS_URL = "http://www.dofus.com/fr/mmorpg/encyclopedie/armes?size=99999"
SETS_URL = "http://www.dofus.com/fr/mmorpg/encyclopedie/panoplies?size=99999"

CATEGORIES = [
    "Arme",
    "Equipement",
    "Familier",
    # "Ressource",
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

ITEM_TYPES = [
    # (CATEGORY , TYPE , JOB)
    ("Equipement", "Amulette", "Bijouter"),
    ("Equipement", "Anneau", "Bijouter"),
    ("Equipement", "Chapeau", "Tailleur"),
    ("Equipement", "Cape", "Tailleur"),
    ("Equipement", "Sac à dos", "Tailleur"),
    ("Equipement", "Ceinture", "Cordonnier"),
    ("Equipement", "Bottes", "Cordonnier"),
    ("Equipement", "Bouclier", "Forgeur de Boucliers"),
    ("Equipement", "Dofus", None),
    
    ("Arme", "Arc", "Sculpteur d'Arcs"),
    ("Arme", "Baguette", "Sculpteur de Baguettes"),
    ("Arme", "Bâton", "Sculpteur de Baton"),
    ("Arme", "Dague", "Forgeur de Dagues"),
    ("Arme", "Épée", "Forgeur d'Epées"),
    ("Arme", "Marteau", "Forgeur de Marteaux"),
    ("Arme", "Pelle", "Forgeur de Pelle"),
    ("Arme", "Hache", "Forgeur de Haches"),
    ("Arme", "Pioche", None),
    ("Arme", "Faux", None),
    ("Arme", "Outil", None),
    ("Arme", "Pierre d'âme", None),
    ("Arme", "Trophée", None),
    
    ("Familier", "Familier", None),
    ("Familier", "Montilier", None),
]

class Command(BaseCommand):
    help = 'Update or rebuild the items database'
    
    option_list = BaseCommand.option_list + (
        make_option('--use-cache',
            dest='use-cache',
            default="y",
            help='(Y/n) Whether to use the web cache or force data refresh'),
        )
        
    def handle(self, *args, **options):
        rebuild_db(options["use-cache"] != "n")
    

def rebuild_db(use_cache=True):
    opener = urllib2.build_opener()
    opener.addheaders.append(('Cookie', DOFUS_COOKIES))
    
    web_cache = WebCache(opener, use_cache)
    
    history = UpdateHistory.objects.create(started=timezone.now(), using_cache=use_cache)
    
#     fetch_items(web_cache, history)
    fetch_sets(web_cache, history)
    
    history.finished = timezone.now()
    history.save()


def fetch_items(web_cache, history):
    build_categories()
    build_jobs()
    build_item_types()
    
    p = MainItemPageParser(web_cache, history)
    p.feed(web_cache.get(WEAPONS_URL))
    p.feed(web_cache.get(STUFF_URL))
    
    
    

def build_categories():
    for c in CATEGORIES:
        log.debug("Inserting category '{}'".format(c))
        ItemCategory.objects.get_or_create(name=c)
    
def build_jobs():
    for j in JOBS:
        log.debug("Inserting job '{}'".format(j))
        Job.objects.get_or_create(name=j)
    
def build_item_types():
    for category, item_type, job in ITEM_TYPES:
        category = ItemCategory.objects.get(name=category)
        if job:
            job = Job.objects.get(name=job)
        
        log.debug("Inserting type '{}'".format(item_type))
        ItemType.objects.get_or_create(name=item_type, category=category, job=job)

def fetch_sets(web_cache, history):
    content = web_cache.get(SETS_URL)
    MainPanopliePageParser(web_cache, history).feed(content)



    