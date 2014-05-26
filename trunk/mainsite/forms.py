from django import forms

class ContactForm(forms.Form):
    sender = forms.EmailField()
    cc_myself = forms.BooleanField(required=False)
    subject = forms.CharField(max_length=100)
    message = forms.CharField(widget=forms.Textarea)
