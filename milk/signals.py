from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Service, Bill
from datetime import datetime
from calendar import monthrange


def last_day_of_month(date_value):
    return date_value.replace(day = monthrange(date_value.year, date_value.month)[1])

@receiver(post_save, sender=Service)
# called when Service model is updated
def my_handler(sender, **kwargs):
    ob = Service.objects.last()     # find the latest record inserted into Service Model

    end_date = ob.date
    start_date = end_date.replace(day=1)

    amount = float()

    if end_date == last_day_of_month(end_date):
        milk_man = ob.milk_man

        # To Do : We must find out first how many milk men were providing service in this month,
        # then for each one we need to generate bill for that month.

        # This is the last entry of the month then generate bill and update Bill model.
        # search all records of this whole month for the given milk man

        # for each milk man:
        #   generate bill
        
        services = Service.objects.all().filter(date__gte = start_date, date__lte = end_date, milk_man=milk_man)
        
        if services:
            for service in services:
                amount += (service.rate.rate * service.quantity)

        # Update Bill model
        bill = Bill(milk_man = milk_man, start_date = start_date, end_date = end_date, amount = amount)
        bill.save()

        print("Rate is {}".format(amount))

