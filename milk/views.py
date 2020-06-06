from django.shortcuts import render, redirect
from .models import Supplier, Service, Bill, Payment
from datetime import datetime, date
from calendar import monthrange
from django.views import View
from .forms import DateSelectForm, SupplyUpdateForm
from enum import IntEnum
from django.contrib import messages


def last_day_of_month(date_value):
    return date_value.replace(day = monthrange(date_value.year, date_value.month)[1])

class ViewType(IntEnum):
    MILK                =       1
    SUPPLY_VIEW         =       2
    SUPPLY_UPDATE       =       3
    BILL_VIEW           =       4
    BILL_UPDATE         =       5
    PAYMENT_VIEW        =       6
    PAYMENT_UPDATE      =       7


class MilkView(View):
    def get(self, request):
        context = {"view_type" : ViewType.MILK}
        return render(request, 'milk/milk.html', context)


class SupplyView(View):
    class ServiceDetail:
        def __init__(self):
            self.id = ''
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

            service_detail.id           =   service.id
            service_detail.supplier     =   service.supplier.name
            service_detail.date         =   service.date
            service_detail.quantity     =   service.quantity
            service_detail.remark       =   service.remark

            service_details.append(service_detail)
    
        return {"view_type" : ViewType.SUPPLY_VIEW, 'supply_view' : service_details, "date_selector" : date_selector}


class SupplyAddView(View):
    def get(self, request):
        update_form = SupplyUpdateForm()

        context = {"view_type" : ViewType.SUPPLY_UPDATE, "supply_update" : update_form}

        return render(request, 'milk/milk.html', context)

    def post(self, request):
        context = dict()

        update_form = SupplyUpdateForm(request.POST)

        if update_form.is_valid():
            update_form.save()
            date = update_form.cleaned_data.get('date')
            context = {"view_type" : ViewType.SUPPLY_UPDATE, "supply_update" : update_form}
            messages.success(request, f"Milk Supply record for '{date}' is added successfully.")
            return redirect('nsmilk:supply_view')
        else:
            messages.error(request, f"Failed to add milk supply record.")
        return render(request, 'milk/milk.html', context)


class SupplyUpdateView(View):
    def get(self, request, pk):
        
        suppy = Service.objects.get(id = pk)

        update_form = SupplyUpdateForm(instance=suppy)

        context = {"view_type" : ViewType.SUPPLY_UPDATE, "supply_update" : update_form}

        return render(request, 'milk/milk.html', context)

    def post(self, request):
        context = dict()

        update_form = SupplyUpdateForm(request.POST)

        if update_form.is_valid():
            update_form.save()
            date = update_form.cleaned_data.get('date')
            context = {"view_type" : ViewType.SUPPLY_UPDATE, "supply_update" : update_form}
            messages.success(request, f"Milk update record for '{date}' is updated successfully.")
            return redirect('nsmilk:supply_view')
        else:
            messages.error(request, f"Failed to update milk supply record.")
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
        
        self.start_date = date(date.today().year, 1, 1)
        self.end_date = date(date.today().year, 12, 31)

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
    
        return {"view_type" : ViewType.BILL_VIEW, 'bill_view' : bill_details, "date_selector" : date_selector}


class BillUpdateView(View):
    def get(self, request):
        date_selector = DateSelectForm()

        context = {"view_type" : ViewType.BILL_UPDATE, "bill_generate" : date_selector}

        return render(request, 'milk/milk.html', context)

    def post(self, request):
        context = dict()
        service_found = False

        date_selector = DateSelectForm(request.POST)

        if date_selector.is_valid():
            start_date = date_selector.cleaned_data['start_date']
            end_date = date_selector.cleaned_data['end_date']

            for supplier in Supplier.objects.all():
                amount = 0

                services = Service.objects.all().filter(
                        date__gte = start_date, 
                        date__lte = end_date,
                        supplier = supplier)

                if services:
                    for service_ob in services:
                        amount += service_ob.quantity * service_ob.rate.rate

                    # Update Bill
                    bill = Bill(supplier = supplier, start_date = start_date,
                                end_date = end_date, amount = amount)

                    bill.save()

                    service_found = True

                    messages.success(request, f"Milk bill for supplier '{supplier.name}', between '{start_date}' and '{end_date}', is generated successfully.")
            
            if not service_found:
                messages.warning(request, f"Skipped generating bill, between '{start_date}' and '{end_date}', as no milk supply found between the given dates.")

            # Find all suppliers who delivered service between the given
            context = {"view_type" : ViewType.BILL_UPDATE, "bill_generate" : date_selector}
            return redirect('nsmilk:bill_view')
        else:
            messages.error(request, f"Failed to generate milk bill.")
        return render(request, 'milk/milk.html', context)


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
    
        return {"view_type" : ViewType.PAYMENT_VIEW, 'payment_details' : payment_details, 'date_selector' : date_selector}


class PaymentPayView(View):
    def get(self, request):
        date_selector = DateSelectForm()

        context = {"payment_view" : date_selector}

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