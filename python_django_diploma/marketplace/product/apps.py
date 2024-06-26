from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ProductConfig(AppConfig):
    name = 'product'
    verbose_name = _('product')
    verbose_name_plural = _('products')
