from django.db import models
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField

from project.models import TimeStampedModel
from user.models import User
from product.models import Product


class Order(TimeStampedModel):
    """ Модель заказа. """

    CREATED = 'CREATED'
    AWAITS_PAYMENT = 'AWAITS_PAYMENT'
    PAID = 'PAID'
    COMPLETED = 'COMPLETED'

    DELIVERY_METHOD = [
        ('ORDINARY', _('ordinary')),
        ('EXPRESS', _('express'))
    ]
    PAYMENT_METHOD = [
        ('ONLINE', _('online')),
        ('SOMEONE', _('someone'))
    ]
    ORDER_STATUS = [
        ('CREATED', _('created')),
        ('AWAITS_PAYMENT', _('awaits_payment')),
        ('PAID', _('paid')),
        ('COMPLETED', _('completed')),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    full_name = models.CharField(max_length=50, blank=True, null=True, verbose_name=_('full name'))
    email = models.EmailField(blank=True, null=True, verbose_name=_('email'))
    phone = PhoneNumberField(blank=True, null=True, verbose_name=_('phone'))
    delivery_type = models.CharField(
        max_length=20,
        choices=DELIVERY_METHOD,
        blank=True,
        verbose_name=_('delivery type')
    )
    payment_type = models.CharField(
        max_length=20,
        choices=PAYMENT_METHOD,
        blank=True,
        verbose_name=_('payment type')
    )
    status = models.CharField(
        max_length=20,
        choices=ORDER_STATUS,
        default='CREATED',
        verbose_name=_('status')
    )
    total_cost = models.IntegerField(default=0, verbose_name=_('total cost'))
    city = models.CharField(blank=True, max_length=50, verbose_name=_('city'))
    address = models.CharField(blank=True, max_length=200, verbose_name=_('address'))
    products = models.ManyToManyField(Product, through='OrderCountProduct')

    class Meta:
        verbose_name_plural = _('order')
        verbose_name = _('order')


class OrderCountProduct(TimeStampedModel):
    """ Модель количество продуктов в заказе. """

    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    count = models.PositiveIntegerField(verbose_name=_('quantity goods'))
    price = models.IntegerField(verbose_name=_('product price'))

    class Meta:
        verbose_name_plural = _('number of product orders')
        verbose_name = _('product order quantity')


class PaymentTransaction(TimeStampedModel):
    """ Модель платежная транзакция. """

    CREATED = 'CREATED'
    PROCESSING = 'PROCESSING'
    ERROR = 'ERROR'
    COMPLETED = 'COMPLETED'

    STATUS_CHOICES = (
        (CREATED, _('created')),
        (ERROR, _('error')),
        (COMPLETED, _('completed'))
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('user'))
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name=_('order'))
    uuid = models.UUIDField(blank=True, null=True, verbose_name=_('uuid'))
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=CREATED,
        verbose_name=_('status')
    )
    error_message = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name=_('error message')
    )

    class Meta:
        verbose_name_plural = _('payment transactions')
        verbose_name = _('payment transaction')
