from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.mail import send_mail

from recaptcha.client import captcha

from smetisufod import settings
from mainsite.models import ItemType
from mainsite.forms import ContactForm

def developers(request):
    page_parameters = {
        "pageTitle": "Smetisufod : Contact",
        "pageDescription": "Smetisufod : Contact",
        "pageUrl": request.build_absolute_uri(),
        "active_tab": "dev",
        "search_full_url": request.build_absolute_uri("search"),
        "plugin_url": request.build_absolute_uri("smetisufod.itemlookup.js"),
        "plugin_css": request.build_absolute_uri("smetisufod.itemlookup.css"),
        "param_list" : [
            {
                "name": ["name"],
                "desc": "La valeur de ce param&egrave;tre sera contenue dans les noms des objets retourn&eacute;s. Non sensible &agrave; la casse.",
                "type": ["Chaine de caract&egrave;re"],
                "example": "/search?name=bouftou",
                "default": "Pas de restriction sur les noms des objets retourn&eacute;s"
            },
            {
                "name": ["type"],
                "desc": "Les types des objets retourn&eacute;s. Ce param&egrave;tre peut &ecirc;tre pr&eacute;sent plusieurs fois pour sp&eacute;cifier les diff&eacute;rents types possibles.",
                "type": list(ItemType.objects.all()),
                "example": "/search?type=Anneau&amp;type=Amulette",
                "default": "Pas de restriction sur les types des objets retourn&eacute;s"
            },
            {
                "name": ["level-min","level-max"],
                "desc": "Les niveaux minimums et maximums des objets retourn&eacute;s.",
                "type": ["Entier"],
                "example": "/search?level-min=10&amp;level-max=20",
                "default": "Pas de restriction sur les niveaux des objets retourn&eacute;s"
            },
            {
                "name": ["recipe"],
                "desc": "Le nombre d'ingr&eacute;dients n&eacute;cessaire pour fabriquer les objets. Ce param&egrave;tre peut &ecirc;tre pr&eacute;sent plusieurs fois pour sp&eacute;cifier les diff&eacute;rents nombres d'ingr&eacute;dients possibles.",
                "type": ["Entier"],
                "example": "/search?recipe=2&amp;recipe=3&amp;recipe=4",
                "default": "Pas de restriction sur les nombres d'ingr&eacute;dients des recettes des objets retourn&eacute;s"
            },
            {
                "name": ["attribute-X"],
                "desc": "Un attribut qui doit &ecirc;tre pr&eacute;sent sur les objets retourn&eacute;s. X est un entier. Peut &ecirc;tre pr&eacute;sent plusieurs fois avec une valeur diff&eacute;rente de X.",
                "type": ["Chaine de caract&egrave;re"],
                "example": "/search?attribute-1=(dommages Neutre)&amp;attribute-2=PA",
                "default": "Pas de restriction sur les attributs que doivent poss&eacute;der les objets retourn&eacute;s"
            },
            {
                "name": ["value-min-X","value-max-X"],
                "desc": "Les valeurs minimales et maximales de l'attribut X. X est un entier. S'il n'existe pas de param&egrave;tre attribute-X correspondant, ces param&egrave;tres sont ignor&eacute;s.",
                "type": ["Entier"],
                "example": "/search?attribute-1=Force&amp;value-min-1=50&amp;value-max-1=70",
                "default": "Pas de restriction sur la valeur de l'attribut X des objets retourn&eacute;s"
            },
            {
                "name": ["include-panoplie"],
                "desc": "Si pr&eacute;sent, inclut les panoplies dans les r&eacute;sultats de recherche.",
                "type": ["on"],
                "example": "/search?include-panoplie=on",
                "default": "Les r&eacute;sultats de recherche n'incluent que les objets"
            },
        ],
        "plugin_option_list": [
            {
                "name": "makeLink",
                "desc": "Si &agrave; true, la cible du plugin sera chang&eacute;e en lien vers ce site vers un r&eacute;sultat de recherche contenant l'objet.",
                "type": ["true", "false"],
                "example": '<span class="code">$(".item-lookup").lookupitem({"makeLink": true});</span> <span class="item-lookup link">Marteau du Bouftou</span>',
                "default": "false"
            },
        ]
    }
    
    return render(request, "developers.html", page_parameters)
