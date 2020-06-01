from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from .forms import UserRegistrationForm


class RegistrationView(View):
    def get(self, request):
        user_creation_form = UserRegistrationForm()
        context = {"user_creation_form" : user_creation_form}
        return render(request, 'userauthentication/userauthentication.html', context)

    def post(self, request):
        user_creation_form = UserRegistrationForm(request.POST)

        if user_creation_form.is_valid():
            user_creation_form.save()
            username = user_creation_form.cleaned_data.get('username')
            messages.success(request, f"Account created successfully for '{username}'")
            return redirect('nsuserauthentication:register')

        context = {"user_creation_form" : user_creation_form}
        return render(request, 'userauthentication/userauthentication.html', context)
