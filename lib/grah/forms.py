"""
Django forms for grah project
"""

from django import forms


class ContactForm(forms.Form):
    subject         =   forms.CharField(max_length=50, 
                                widget=forms.TextInput(
                                    attrs=
                                    {
                                        "placeholder" : "Enter the Subject",
                                        "class" : "form-control-sm",
                                        "type" : "text"
                                    }
                                    ))
    message         =   forms.CharField(
                            widget=forms.Textarea(
                                attrs=
                                {"rows": 3, "cols":20, "class" : "form-control-sm", "placeholder" : "Enter the Message"}
                                ))
    sender        =   forms.EmailField(widget=forms.TextInput(
                                    attrs=
                                    {
                                        "placeholder" : "Enter your email address."
                                    }))
    cc_yourself       =   forms.BooleanField(required = False)