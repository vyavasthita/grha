from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from .forms import UserRegistrationForm


class RegistrationView(View):
    def get(self, request):
        user_creation_form = UserRegistrationForm()
        context = {"user_creation_form" : user_creation_form}
        return render(request, 'userauthentication/registeration.html', context)

    def post(self, request):
        user_creation_form = UserRegistrationForm(request.POST)

        if user_creation_form.is_valid():
            user_creation_form.save()
            username = user_creation_form.cleaned_data.get('username')
            messages.success(request, f"Hi '{username}', Your account has been created successfully. You can login now.")
            return redirect('nsuserauthentication:login')

        context = {"user_creation_form" : user_creation_form}
        return render(request, 'userauthentication/registeration.html', context)

    
class ProfileView(LoginRequiredMixin, View):
    template_name = "userauthentication/profile.html"

    def get(self, request):
        return render(request, self.template_name)
