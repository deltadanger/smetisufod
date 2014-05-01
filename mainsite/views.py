import json, logging

log = logging.getLogger(__name__)

from annoying.decorators import render_to
from django.db.models import Q
from django.http import HttpResponse
from django.core import serializers

from mainsite.models import Attribute, ItemCategory, ItemType, Item

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


@render_to()
def home(request):
    
    attributes = Attribute.objects.all().order_by("name")
    categories = ItemCategory.objects.all()
    
    return {
        "attributes": attributes,
        "categories": categories,
        'TEMPLATE': "search.html",
    }

def search(request):
    print request.GET
    types = json.loads(request.GET.get("types"))
    
    type_query = Q()
    for type in types:
        if type == "all":
            type_list = ItemType.objects.all()
        
        if type.startswith("cat-"):
            type_list = ItemType.objects.filter(category__name=type[4:])
            
        if type.startswith("type-"):
            type_list = [ItemType.objects.get(name=type[5:])]
        
        type_query |= Q(type__in=type_list)
    
    
    name = request.GET.get("name")
    name_query = Q()
    if name:
        name_query = Q(name__icontains=name)
    
    
    level_min = request.GET.get("level_min", "1")
    level_max = request.GET.get("level_max", "200")
    level_query = Q(level__gte=int(level_min), level__lte=int(level_max))
    
    
    recipes = request.GET.getlist("recipes")
    recipe_query = Q()
    for recipe in recipes:
        recipe_query |= Q(recipe__size=recipe)
    
    
    attributes = json.loads(request.GET.get("attributes"))
    include_panoplie = request.GET.get("include_panoplie")
    
    attribute_query = Q()
    for attr in attributes:
        attributeObject = Attribute.objects.get_if_exist(name=attr["value"])
        
        if not attributeObject:
            continue
        
        if not attr["min"]:
            attr["min"] = 1
        
        if not attr["max"]:
            attr["max"] = 9999
        
        query = Q(attributevalue__attribute=attributeObject,
                  attributevalue__min_value__lte=attr["max"],
                  attributevalue__max_value__gte=attr["min"])
        
        if include_panoplie:
            query |= Q(panoplie__panoplieattribute__attribute=attributeObject,
                       panoplie__panoplieattribute__value__lte=attr["max"],
                       panoplie__panoplieattribute__value__gte=attr["min"])
        
        attribute_query &= query
    
    
    items = Item.objects.filter(type_query & name_query & level_query & recipe_query & attribute_query).distinct()
    
    
    log.debug(type_query)
    log.debug(name_query)
    log.debug(level_query)
    log.debug(recipe_query)
    log.debug(attribute_query)
    log.debug(items)
    
    return HttpResponse(json.dumps([dictify(item) for item in items]), mimetype="application/json");
    
    return HttpResponse(serializers.serialize("json", items), mimetype="application/json");
    

def dictify(item):
    result = {}
    result["name"] = item.name
    result["description"] = item.description
    result["original_id"] = item.original_id
    result["type"] = item.type.name
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
            attributes.append(str(a.min_value) + "-" + str(a.max_value) + " " + a.attribute.name)
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
    
    
    
    
    
    
    
    
    




