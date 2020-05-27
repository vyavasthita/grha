"""
Django forms for grah project
"""

from django import forms


class ContactForm(forms.Form):
    subject         =   forms.CharField(max_length=50)
    message         =   forms.CharField(widget=forms.Textarea)
    my_email        =   forms.EmailField()
    cc_myself       =   forms.BooleanField(required = False)