from django.shortcuts import render
from .models import MilkMan, Service

class ServiceDetail:
    def __init__(self):
        self.milk_man = ''
        self.date = ''
        self.quantity = ''
        self.remark = ''

def milk(request):
    service_details = list()

    for service in Service.objects.all():
        service_detail              =   ServiceDetail()
        service_detail.milk_man     =   service.milk_men.name
        service_detail.date         =   service.date
        service_detail.quantity     =   service.quantity
        service_detail.remark       =   service.remark

        service_details.append(service_detail)

    context = {'service_details' : service_details}
    return render(request, 'milk/milk.html', context)
