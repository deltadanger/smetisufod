
from annoying.decorators import render_to


@render_to()
def home(request):
    
    return {
        'TEMPLATE': "search.html",
    }


