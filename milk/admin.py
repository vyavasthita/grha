from django.contrib import admin
from .models import MilkMan, Rate, Service, Bill, Payment


admin.site.register(MilkMan)
admin.site.register(Rate)
admin.site.register(Service)
admin.site.register(Bill)
admin.site.register(Payment)
