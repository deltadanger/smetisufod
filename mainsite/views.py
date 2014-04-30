
from annoying.decorators import render_to
from django.http import HttpResponse

from mainsite.models import Attribute, ItemCategory

@render_to()
def home(request):
    
    attributes = Attribute.objects.all().order_by("name__fr_fr")
    categories = ItemCategory.objects.all()
    
    return {
        "attributes": attributes,
        "categories": categories,
        'TEMPLATE': "search.html",
    }

def search(request):
    
    return HttpResponse(request.GET.get("test"))
    





