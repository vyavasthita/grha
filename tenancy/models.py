from django.db import models


class Tenant(models.Model):
    name        =       models.CharField(max_length=30)
    sex         =       models.CharField(max_length=1)
    address     =       models.CharField(max_length=300)
    phone       =       models.BigIntegerField(unique=True)


class Room(models.Model):
    name        =   models.CharField(max_length=30)
    rent        =   models.FloatField()
    rent_type   =   models.CharField(max_length=1, default='A')
    rent_date   =   models.SmallIntegerField(default=1)


class Occupency(models.Model):
    rent        =   models.ForeignKey(Room, on_delete = models.CASCADE)
    tenant      =   models.ForeignKey(Tenant, on_delete = models.CASCADE)
    rent_month  =   models.DateField()
    start_date  =   models.DateField()
    end_date    =   models.DateField()
    payment     =   models.FloatField()
    status      =   models.BooleanField()
    remarks     =   models.CharField(max_length=500, default = '')
