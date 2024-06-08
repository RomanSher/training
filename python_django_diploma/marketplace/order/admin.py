from django.contrib import admin
from modeltranslation.admin import TranslationAdmin
from modeltranslation.translator import TranslationOptions, register

from order.models import Order, OrderCountProduct, PaymentTransaction
from project.djnago_admin.admin import UserModelAdmin, OrderModelAdmin, ProductModelAdmin


@register(OrderCountProduct)
class OrderCountProductTranslationOptions(TranslationOptions):
    fields = ('price',)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'full_name', 'delivery_type',
        'payment_type', 'status', 'total_cost'
    )
    search_fields = ('id', 'user__username', 'email', 'full_name')
    list_filter = ('status', 'delivery_type', 'payment_type')


@admin.register(OrderCountProduct)
class OrderCountProductAdmin(OrderModelAdmin, ProductModelAdmin, TranslationAdmin):
    list_display = ('id', 'show_order', 'count', 'price', 'show_product')
    search_fields = ('id', 'order_id')


@admin.register(PaymentTransaction)
class PaymentTransactionAdmin(UserModelAdmin, OrderModelAdmin):
    list_display = ('id', 'show_user', 'show_order', 'status')
    search_fields = ('id', 'user__username', 'user__email', 'order_id')
    list_filter = ('status',)
