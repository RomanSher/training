from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class BasketConfig(AppConfig):
    name = 'basket'
    verbose_name = _('basket')