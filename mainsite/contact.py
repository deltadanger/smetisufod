from django.shortcuts import render
from django.core.mail import send_mail

from recaptcha.client import captcha

from smetisufod import settings
from mainsite.forms import ContactForm
from smetisufod.private_settings import RECAPTCHA_PRIVATE_KEY

def contact(request):
    page_parameters = {
        "pageTitle": "Smetisufod : Contact",
        "pageDescription": "Smetisufod : Contact",
        "pageUrl": "",
        "active_tab": "contact",
        "captcha_key": settings.RECAPTCHA_PUBLIC_KEY
    }
    
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            response = captcha.submit(
                request.POST.get('recaptcha_challenge_field'),
                request.POST.get('recaptcha_response_field'),
                RECAPTCHA_PRIVATE_KEY,
                request.META['REMOTE_ADDR'],)
          
            # see if the user correctly entered CAPTCHA information
            # and handle it accordingly.
            if response.is_valid:
                recipients = ["delta.danger@gmail.com"]
                
                send_mail(form.cleaned_data["subject"],
                          form.cleaned_data["body"],
                          form.cleaned_data["sender"],
                          recipients,
                          fail_silently=False)
             
            page_parameters.update({"sent": True,})
            return render(request, "contact.html", page_parameters)
    else:
        form = ContactForm()

    page_parameters.update({"form": form,})
    return render(request, "contact.html", page_parameters)
