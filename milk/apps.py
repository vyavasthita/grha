from django.apps import AppConfig
from django.db.models.signals import post_save
from django.utils.translation import ugettext_lazy as _


class MilkConfig(AppConfig):
    name = 'milk'
    verbose_name = _('milk')

    def ready(self):
        from .signals import my_handler
        post_save.connect(my_handler, sender='milk.Service')