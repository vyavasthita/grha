# Generated by Django 3.0.6 on 2020-05-23 02:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tenancy', '0004_auto_20200523_0242'),
    ]

    operations = [
        migrations.AlterField(
            model_name='occupency',
            name='start_date',
            field=models.DateField(auto_now=True),
        ),
    ]