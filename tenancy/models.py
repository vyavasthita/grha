from django.db import models
from datetime import date


class Tenant(models.Model):
    name            =       models.CharField(max_length=30)
    sex             =       models.CharField(max_length=1)
    address         =       models.CharField(max_length=300)
    phone           =       models.BigIntegerField(unique=True)

    def __str__(self):
        return self.name
    

class Property(models.Model):
    name            =       models.CharField(max_length=50)
    address         =       models.CharField(max_length=200)
    rent            =       models.FloatField()
    rent_type       =       models.CharField(max_length=1, default='A')
    rent_date       =       models.SmallIntegerField(default=1)

    def __str__(self):
        return self.name
    

class Occupency(models.Model):
    property        =       models.ForeignKey(Property, on_delete = models.CASCADE)
    tenant          =       models.ForeignKey(Tenant, on_delete = models.CASCADE)
    start_date      =       models.DateField(default = date.today)
    end_date        =       models.DateField()

    def __str__(self):
        return str(self.property) + '_' + str(self.tenant)
    

class Rent(models.Model):
    occupency       =       models.ForeignKey(Occupency, on_delete = models.CASCADE)
    rent_month      =       models.DateField()
    payment_date    =       models.DateField(default = date.today)
    amount          =       models.FloatField()
    remark          =       models.CharField(max_length=1000, blank=True)

    def __str__(self):
        return str(self.occupency)
    
