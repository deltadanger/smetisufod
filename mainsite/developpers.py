from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.mail import send_mail

from recaptcha.client import captcha

from smetisufod import settings
from mainsite.forms import ContactForm

def developpers(request):
    page_parameters = {
        "pageTitle": "Smetisufod : Contact",
        "pageDescription": "Smetisufod : Contact",
        "pageUrl": "",
        "active_tab": "dev"
    }
    
    return render(request, "developpers.html", page_parameters)
