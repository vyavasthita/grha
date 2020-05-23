from django.shortcuts import render
from .models import Rent


def tenancy(request):
    rent = Rent.objects.all()
    context = {'rent': rent}
    return render(request, 'tenancy/tenancy.html', context)