from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class OrderConfig(AppConfig):
    name = 'order'
    verbose_name = _('order')
    verbose_name_plural = _('orders')