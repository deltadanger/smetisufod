
from django.shortcuts import render_to_response
from django.template import RequestContext

def js(request):
    params = {
        "get_item_uri": request.build_absolute_uri("get_item"),
        "search_uri": request.build_absolute_uri("search.html"),
    }
    return render_to_response("smetisufod.itemlookup.js", params, context_instance=RequestContext(request), mimetype="application/javascript")



def css(request):
    params = {}
    return render_to_response("smetisufod.itemlookup.css", params, context_instance=RequestContext(request), mimetype="text/css")
