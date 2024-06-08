from django.db import models
from django.utils.translation import gettext_lazy as _

from project.models import TimeStampedModel
from user.models import User
from product.models import Product


class Basket(TimeStampedModel):
    """ Модель корзина заказов. """

    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name=_('product'))
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('user'))
    count = models.IntegerField(default=0, verbose_name=_('quantity goods'))
    price = models.IntegerField(default=0, verbose_name=_('product price'))

    class Meta:
        verbose_name = _('basket')
        verbose_name_plural = _('baskets')
