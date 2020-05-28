from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Supplier, Service, Bill
from datetime import datetime
from calendar import monthrange


def last_day_of_month(date_value):
    return date_value.replace(day = monthrange(date_value.year, date_value.month)[1])

def generate_service_list():
    pass

def get_suppliers():
    pass

def get_bill_amt(services):
    amount = 0

    for service in services:
        amount += (service.rate.rate * service.quantity)

    return amount

def update_bill(start_date, end_date):  # Update Bill model
    # To Do : We must find out first how many milk suppliers were providing service in this month,
    # then for each one we need to generate bill for that month.

    # This is the last entry of the month then generate bill and update Bill model.
    # search all records of this whole month for the given milk supplier

    # for each milk man:
    #   generate bill

    for supplier in Supplier.objects.all():
        services = Service.objects.all().filter(date__gte = start_date, date__lte = end_date, supplier=supplier)
        
        if services:
            amount = get_bill_amt(services)

            # Update Bill model
            bill = Bill(supplier = supplier, start_date = start_date, end_date = end_date, amount = amount)
            bill.save()

@receiver(post_save, sender=Service)
# called when Service model is updated
def my_handler(sender, **kwargs):
    ob = Service.objects.last()     # find the latest record inserted into Service Model

    end_date = ob.date
    start_date = end_date.replace(day=1)

    if end_date == last_day_of_month(end_date):
        update_bill(start_date, end_date)



