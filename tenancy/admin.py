from django.contrib import admin

from .models import Tenant, Property, Occupency, Rent

# Register your models here.
admin.site.register(Tenant)
admin.site.register(Property)
admin.site.register(Occupency)
admin.site.register(Rent)
