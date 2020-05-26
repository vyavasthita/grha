from django.contrib import admin
from .models import Supplier, Rate, Service, Bill, Payment


admin.site.register(Supplier)
admin.site.register(Rate)
admin.site.register(Service)
admin.site.register(Bill)
admin.site.register(Payment)
