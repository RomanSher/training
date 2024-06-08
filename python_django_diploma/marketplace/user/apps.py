from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class UserConfig(AppConfig):
    name = 'user'
    verbose_name = _('user')
    verbose_name_plural = _('users')

    def ready(self):
        import user.signals
