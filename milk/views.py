from django.shortcuts import render
from .models import Supplier, Service, Bill, Payment
from datetime import datetime
from calendar import monthrange
from django.views import View
from .forms import DateSelectForm, SupplyUpdateForm


def last_day_of_month(date_value):
    return date_value.replace(day = monthrange(date_value.year, date_value.month)[1])


class MilkView(View):
    def get(self, request):
        context = {"milk_view" : 1}
        return render(request, 'milk/milk.html', context)


class SupplyView(View):

    class ServiceDetail:
        def __init__(self):
            self.supplier = ''
            self.date = ''
            self.quantity = ''
            self.remark = ''
            
    def __init__(self):
        super(SupplyView, self).__init__()

        self.template_name = 'milk/milk.html'
        self.form_class = DateSelectForm
        
        self.start_date = datetime.today().replace(day=1)
        self.end_date = last_day_of_month(datetime.today().date())

    def get(self, request):
        date_selector = self.form_class()
        context = self.process_request(date_selector)

        return render(request, self.template_name, context)
    
    def post(self, request):
        date_selector = self.form_class(request.POST)

        if date_selector.is_valid():
            self.start_date = date_selector.cleaned_data['start_date']
            self.end_date = date_selector.cleaned_data['end_date']

        context = self.process_request(date_selector)

        return render(request, self.template_name, context)

    def process_request(self, date_selector):
        service_details = list()
    
        for service in Service.objects.all().filter(
            date__gte = self.start_date, 
            date__lte = self.end_date).order_by('date'):
            service_detail              =   SupplyView.ServiceDetail()

            service_detail.supplier     =   service.supplier.name
            service_detail.date         =   service.date
            service_detail.quantity     =   service.quantity
            service_detail.remark       =   service.remark

            service_details.append(service_detail)
    
        return {'supply_view' : service_details, "date_selector" : date_selector}


class SupplyUpdateView(View):
    def get(self, request):
        update_form = SupplyUpdateForm()

        context = {"supply_update" : update_form}

        return render(request, 'milk/milk.html', context)

    def post(self, request):
        context = dict()

        update_form = SupplyUpdateForm(request.POST)

        if update_form.is_valid():
            update_form.save()
            context = {"supply_update" : update_form}

        return render(request, 'milk/milk.html', context)


class BillView(View):
    class BillDetail:
        def __init__(self):
            self.supplier = ''
            self.start_date = ''
            self.end_date = ''
            self.amount = ''

    def __init__(self):
        super(BillView, self).__init__()

        self.template_name = 'milk/milk.html'
        self.form_class = DateSelectForm
        
        self.start_date = datetime.today().replace(day=1)
        self.end_date = last_day_of_month(datetime.today().date())

    def get(self, request):
        date_selector = self.form_class()
        context = self.process_request(date_selector)

        return render(request, self.template_name, context)
    
    def post(self, request):
        date_selector = self.form_class(request.POST)

        if date_selector.is_valid():
            self.start_date = date_selector.cleaned_data['start_date']
            self.end_date = date_selector.cleaned_data['end_date']

        context = self.process_request(date_selector)

        return render(request, self.template_name, context)

    def process_request(self, date_selector):
        bill_details = list()

        for bill in Bill.objects.all().filter(start_date__gte = self.start_date, end_date__lte = self.end_date).order_by('start_date'):
            bill_detail                 =   BillView.BillDetail()

            bill_detail.supplier        =   bill.supplier.name
            bill_detail.start_date      =   bill.start_date
            bill_detail.end_date        =   bill.end_date
            bill_detail.amount          =   bill.amount

            bill_details.append(bill_detail)
    
        return {'bill_view' : bill_details, "date_selector" : date_selector}


class BillUpdateView(View):
    def get(self, request):
        date_selector = DateSelectForm()

        context = {"bill_generate" : date_selector}

        return render(request, 'milk/milk.html', context)

    def post(self, request):
        context = dict()

        date_selector = DateSelectForm(request.POST)

        if date_selector.is_valid():
            start_date = date_selector.cleaned_data['start_date']
            end_date = date_selector.cleaned_data['end_date']

            for supplier in Supplier.objects.all():
                amount = 0

                for service_ob in Service.objects.all().filter(
                        date__gte = start_date, 
                        date__lte = end_date,
                        supplier = supplier):
                    amount += service_ob.quantity * service_ob.rate.rate

                # Update Bill
                bill = Bill(supplier = supplier, start_date = start_date,
                            end_date = end_date, amount = amount)

                bill.save()

            # Find all suppliers who delivered service between the given
            context = {"bill_generate" : date_selector}

        return render(request, 'milk/milk.html', context)


# class BillDetail:
#     def __init__(self):
#         self.supplier = ''
#         self.start_date = ''
#         self.end_date = ''
#         self.amount = ''


# def bill(request):
#     start_date = datetime.today().replace(day=1)
#     end_date = last_day_of_month(datetime.today().date())

#     if request.method == "POST":
#         filter_start_date = request.POST.get('start_date')      # Start date in 'str' format
#         filter_end_date = request.POST.get('end_date')          # End date in 'str' format
#         date_format = '%Y-%m-%d'

#         if filter_start_date and filter_end_date:       # Both dates provided
#             start_date = datetime.strptime(filter_start_date, date_format).date()        # Convert 'str' to 'date' object
#             end_date = datetime.strptime(filter_end_date, date_format).date()        # Convert 'str' to 'date' object

#     bill_details = list()

#     for bill in Bill.objects.all().filter(start_date__gte = start_date, end_date__lte = end_date).order_by('start_date'):
#         bill_detail                 =   BillDetail()
#         bill_detail.supplier        =   bill.supplier.name
#         bill_detail.start_date      =   bill.start_date
#         bill_detail.end_date        =   bill.end_date
#         bill_detail.amount          =   bill.amount

#         bill_details.append(bill_detail)

#     context = {'bill_details' : bill_details}
#     return render(request, 'milk/bill.html', context)

# def payment(request):
#     context = {'payment_details' : "temp"}
#     return render(request, 'milk/payment.html', context)

class PaymentView(View):
    class PaymentDetail:
        def __init__(self):
            self.supplier = ''
            self.amount = ''
            self.payment_date = ''
            self.remaining_amt = ''
            self.remark = ''

    def __init__(self):
        super(PaymentView, self).__init__()

        self.template_name = 'milk/milk.html'
        self.form_class = DateSelectForm
        
        self.start_date = datetime.today().replace(day=1)
        self.end_date = last_day_of_month(datetime.today().date())

    def get(self, request):
        date_selector = self.form_class()
        context = self.process_request(date_selector)

        return render(request, self.template_name, context)
    
    def post(self, request):
        date_selector = self.form_class(request.POST)

        if date_selector.is_valid():
            self.start_date = date_selector.cleaned_data['start_date']
            self.end_date = date_selector.cleaned_data['end_date']

        context = self.process_request(date_selector)

        return render(request, self.template_name, context)

    def process_request(self, date_selector):
        payment_details = list()

        for bill in Payment.objects.all():
            for payment in Payment.objects.all().filter(bill = bill).order_by('payment_date'):
                payment_detail                 =   PaymentView.PaymentDetail()

                payment_detail.supplier        =   payment.bill.supplier.name
                payment_detail.amount          =   payment.start_date
                payment_detail.payment_date    =   payment.payment_date
                payment_detail.remaining_amt   =   payment.remaining_amt
                payment_detail.remark          =   payment.remark

                payment_details.append(payment_detail)
    
        return {'payment_view' : payment_details, "date_selector" : date_selector}


class PaymentPayView(View):
    def get(self, request):
        date_selector = DateSelectForm()

        context = {"bill_generate" : date_selector}

        return render(request, 'milk/milk.html', context)

    def post(self, request):
        context = dict()

        date_selector = DateSelectForm(request.POST)

        if date_selector.is_valid():
            start_date = date_selector.cleaned_data['start_date']
            end_date = date_selector.cleaned_data['end_date']

            for supplier in Supplier.objects.all():
                amount = 0

                for service_ob in Service.objects.all().filter(
                        date__gte = start_date, 
                        date__lte = end_date,
                        supplier = supplier):
                    amount += service_ob.quantity * service_ob.rate.rate

                # Update Bill
                bill = Bill(supplier = supplier, start_date = start_date,
                            end_date = end_date, amount = amount)

                bill.save()

            # Find all suppliers who delivered service between the given
            context = {"bill_generate" : date_selector}

        return render(request, 'milk/milk.html', context)