import json, logging

log = logging.getLogger(__name__)

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.db.models import Q
from django.http import HttpResponse
from django.core import serializers

from mainsite.models import Attribute, ItemCategory, ItemType, Item, Panoplie, PanoplieAttribute

EXCLUDE_CATEGORY = ["Ressource"]
RECIPE_SIZE_TO_JOB_LEVEL = {
    1: 1,
    2: 1,
    3: 10,
    4: 20,
    5: 40,
    6: 60,
    7: 80,
    8: 100
}

def home(request):
    attributes = Attribute.objects.all().order_by("name")
    categories = ItemCategory.objects.all()
    
    return render_to_response("search.html", {
            "attributes": attributes,
            "categories": categories,
        }, context_instance=RequestContext(request)
    )

def search(request):
    print request.GET
    types = json.loads(request.GET.get("types"))
    
    type_query = Q()
    type_query_pano = Q()
    for type in types:
        type_list = None
        
        if type.startswith("cat-"):
            type_list = ItemType.objects.filter(category__name=type[4:])
            
        if type.startswith("type-"):
            type_list = [ItemType.objects.get(name=type[5:])]
        
        if type_list:
            type_query |= Q(type__in=type_list)
            type_query_pano |= Q(item__type__in=type_list)
            
    
    
    name = request.GET.get("name")
    name_query = Q()
    if name:
        name_query = Q(name__icontains=name)
    
    
    level_min = request.GET.get("level_min", "1")
    level_max = request.GET.get("level_max", "200")
    level_query = Q(level__gte=int(level_min), level__lte=int(level_max))
    level_query_pano = Q(item__in=Item.objects.filter(level__lte=level_max) & Item.objects.filter(level__gte=level_min))
    
    
    recipes = request.GET.getlist("recipes[]")
    recipe_query = Q()
    for recipe in recipes:
        recipe_query |= Q(recipe__size=recipe)
    
    
    attributes = json.loads(request.GET.get("attributes"))
    
    attribute_querys = []
    attribute_querys_pano = []
    for attr in attributes:
        attributeObject = Attribute.objects.get_if_exist(name=attr["value"])
        
        if not attributeObject:
            continue
        
        if not attr["min"]:
            attr["min"] = 1
        
        if not attr["max"]:
            attr["max"] = 9999
        
        attribute_querys.append(Q(attributevalue__attribute=attributeObject,
                                 attributevalue__min_value__lte=attr["max"],
                                 attributevalue__max_value__gte=attr["min"]))
        
        attribute_querys_pano.append(Q(panoplieattribute__attribute=attributeObject,
                                      panoplieattribute__value__lte=attr["max"],
                                      panoplieattribute__value__gte=attr["min"]))
    
    
    items = Item.objects.filter(type_query & name_query & level_query & recipe_query)
    for q in attribute_querys:
        items = items.filter(q)
    items = items.distinct()
    
    
    panoplies = []
    if request.GET.get("include_panoplie") and not recipes:
        panoplies = Panoplie.objects.filter(name_query & type_query_pano & level_query_pano)
        for q in attribute_querys_pano:
            panoplies = panoplies.filter(q)
        panoplies = panoplies.distinct()
        
    
    log.debug(type_query)
    log.debug(name_query)
    log.debug(level_query)
    log.debug(recipe_query)
    log.debug(attribute_querys)
    log.debug(items)
    
    log.debug(type_query_pano)
    log.debug(level_query_pano)
    log.debug(attribute_querys_pano)
    log.debug(panoplies)
    
    
    
    
    return HttpResponse(json.dumps([dictify_item(item) for item in items] + [dictify_pano(pano) for pano in panoplies]), mimetype="application/json");
    
    return HttpResponse(serializers.serialize("json", items), mimetype="application/json");
    

def dictify_item(item):
    result = {}
    result["is_item"] = True
    result["name"] = item.name
    result["description"] = item.description
    result["original_id"] = item.original_id
    result["type"] = item.type.name
    result["is_weapon"] = item.type.category.name == "Arme"
    result["level"] = item.level
    result["cost"] = item.cost
    result["range"] = item.range
    result["crit_chance"] = item.crit_chance
    result["crit_damage"] = item.crit_damage
    result["failure"] = item.failure
    result["job"] = ""
    if item.type.job:
        result["job"] = item.type.job.name
        
    result["job_level"] = 0
    result["recipe"] = ""
    if item.recipe:
        result["job_level"] = RECIPE_SIZE_TO_JOB_LEVEL.get(item.recipe.size)
        result["recipe"] = item.recipe.text
    
    attributes = []
    for a in item.attributevalue_set.all().order_by("attribute__name"):
        if a.min_value != a.max_value:
            attributes.append(str(a.min_value) + " - " + str(a.max_value) + " " + a.attribute.name)
        else:
            attributes.append(str(a.min_value) + " " + a.attribute.name)
    result["attributes"] = attributes
    
    conditions = []
    for c in item.attributecondition_set.all().order_by("attribute__name"):
        conditions.append(c.attribute.name + " " + c.equality + " " + str(c.required_value))
    
    result["conditions"] = conditions
    
    if item.panoplie:
        result["panoplie"] = item.panoplie.name
    
    return result

def dictify_pano(pano):
    result = {}
    result["is_item"] = False
    result["name"] = pano.name
    
    attributes = {}
    for a in pano.panoplieattribute_set.all().order_by("attribute__name"):
        if not attributes.has_key(a.no_of_items):
            attributes[a.no_of_items] = []
        
        attributes[a.no_of_items].append(str(a.value) + " " + a.attribute.name)
    
    result["attributes"] = attributes
    
    result["items"] = list(pano.item_set.all().values_list('name', flat=True))
    result["level"] = max(pano.item_set.values_list("level", flat=True))
    
    return result















