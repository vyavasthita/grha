from django.shortcuts import render


def tenancy(request):
    print(request)
    return render(request, 'tenancy/tenancy.html')