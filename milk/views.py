from django.shortcuts import render
from .models import Supplier, Service, Bill, Payment
from datetime import datetime
from calendar import monthrange


class ServiceDetail:
    def __init__(self):
        self.supplier = ''
        self.date = ''
        self.quantity = ''
        self.remark = ''

class BillDetail:
    def __init__(self):
        self.supplier = ''
        self.start_date = ''
        self.end_date = ''
        self.amount = ''

def last_day_of_month(date_value):
    return date_value.replace(day = monthrange(date_value.year, date_value.month)[1])

def supply(request):
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
    services = Service.objects.all().filter(date__gte = start_date, date__lte = end_date).order_by('date')
    
    if services:
        for service in services:
            service_detail              =   ServiceDetail()
            service_detail.supplier     =   service.supplier.name
            service_detail.date         =   service.date
            service_detail.quantity     =   service.quantity
            service_detail.remark       =   service.remark

            service_details.append(service_detail)

    context = {'service_details' : service_details}
    return render(request, 'milk/supply.html', context)

def bill(request):
    start_date = datetime.today().replace(day=1)
    end_date = last_day_of_month(datetime.today().date())

    if request.method == "POST":
        filter_start_date = request.POST.get('start_date')      # Start date in 'str' format
        filter_end_date = request.POST.get('end_date')          # End date in 'str' format
        date_format = '%Y-%m-%d'

        if filter_start_date and filter_end_date:       # Both dates provided
            start_date = datetime.strptime(filter_start_date, date_format).date()        # Convert 'str' to 'date' object
            end_date = datetime.strptime(filter_end_date, date_format).date()        # Convert 'str' to 'date' object

    bill_details = list()

    for bill in Bill.objects.all().filter(start_date__gte = start_date, end_date__lte = end_date).order_by('start_date'):
        bill_detail                 =   BillDetail()
        bill_detail.supplier        =   bill.supplier.name
        bill_detail.start_date      =   bill.start_date
        bill_detail.end_date        =   bill.end_date
        bill_detail.amount          =   bill.amount

        bill_details.append(bill_detail)

    context = {'bill_details' : bill_details}
    return render(request, 'milk/bill.html', context)

def payment(request):
    context = {'payment_details' : "temp"}
    return render(request, 'milk/payment.html', context)