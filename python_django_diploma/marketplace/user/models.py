from typing import Dict

from django.db import models
from django.contrib.auth.models import AbstractUser, User
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField
from rest_framework_simplejwt.tokens import RefreshToken


class User(AbstractUser):
    """ Модель пользователя. """

    full_name = models.CharField(max_length=50, verbose_name=_('full name'))
    email = models.EmailField(unique=True, verbose_name=_('email'))
    phone = PhoneNumberField(unique=True, blank=True, null=True, verbose_name=_('phone'))
    avatar = models.ImageField(upload_to='profile/', blank=True, null=True, verbose_name=_('avatar'))

    class Meta:
        verbose_name_plural = _('user')
        verbose_name = _('user')

    def __str__(self):
        return self.full_name

    @staticmethod
    def refresh_token_user(user: User) -> Dict:
        """
        Создает новый токен доступа для пользователя и возвращает
        его в виде словаря.
        :param user: Пользователь, для которого необходимо обновить
        токен доступа.
        :return: Словарь с новым токеном доступа.
        """
        token = RefreshToken.for_user(user)
        return {'access': str(token.access_token)}
