from django.contrib import admin
from modeltranslation.admin import TranslationAdmin
from modeltranslation.translator import TranslationOptions, register

from basket.models import Basket
from project.djnago_admin.admin import ProductModelAdmin, UserModelAdmin


@register(Basket)
class BasketTranslationOptions(TranslationOptions):
    fields = ('price',)


@admin.register(Basket)
class BasketAdmin(ProductModelAdmin, UserModelAdmin, TranslationAdmin):
    list_display = ('id', 'show_product', 'show_user', 'count', 'price')
    search_fields = ('id', 'user__username', 'user__email', 'user__full_name')
