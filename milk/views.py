from django.shortcuts import render
from .models import MilkMan, Service
from datetime import datetime
from calendar import monthrange


class ServiceDetail:
    def __init__(self):
        self.milk_man = ''
        self.date = ''
        self.quantity = ''
        self.remark = ''

def last_day_of_month(date_value):
    return date_value.replace(day = monthrange(date_value.year, date_value.month)[1])
 
def milk(request):
    start_date = datetime.today().replace(day=1)
    end_date = last_day_of_month(datetime.today().date())

    if request.method == "POST":
        filter_start_date = request.POST.get('start_date')      # Start date in 'str' format
        filter_end_date = request.POST.get('end_date')          # End date in 'str' format
        date_format = '%Y-%m-%d'

        if filter_start_date and filter_end_date:       # Both dates provided
            start_date = datetime.strptime(filter_start_date, date_format).date()        # Convert 'str' to 'date' object
            end_date = datetime.strptime(filter_end_date, date_format).date()        # Convert 'str' to 'date' object

    service_details = list()
    services = Service.objects.all().filter(date__gte = start_date, date__lte = end_date)
    
    if services:
        for service in services:
            service_detail              =   ServiceDetail()
            service_detail.milk_man     =   service.milk_man.name
            service_detail.date         =   service.date
            service_detail.quantity     =   service.quantity
            service_detail.remark       =   service.remark

            service_details.append(service_detail)

    context = {'service_details' : service_details}
    return render(request, 'milk/milk.html', context)
