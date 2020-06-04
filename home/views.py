from django.shortcuts import render
from django.http import HttpResponseRedirect
from lib.grah.forms import ContactForm
from django.core.mail import send_mail
from decouple import config, Csv        # Please update .env file or config vars on Heroku


def contact(request):
    contact = None

    # if this is a POST request we need to process the form data
    if request.method == "POST":
        # create a form instance and populate it with data from the request
        contact = ContactForm(request.POST)

        # check whether it's valid
        if contact.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
    
            subject         =   contact.cleaned_data['subject']
            message         =   contact.cleaned_data['message']
            sender          =   contact.cleaned_data['sender']
            cc_yourself     =   contact.cleaned_data['cc_yourself']
            
            recipients = config('EMAIL_RECIPIENTS', cast=Csv())

            if cc_yourself:
                recipients.append(sender)

            send_mail(subject, message, sender, recipients)
            return HttpResponseRedirect('/thanks/')

    else:   # GET request
        contact = ContactForm()

    context = {'contact' : contact}

    return render(request, 'home/contact.html', context)

def thanks(request):
    return render(request, 'home/thanks.html')

def home(request):
    return render(request, 'home/home.html')