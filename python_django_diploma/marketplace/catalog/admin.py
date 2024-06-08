from django.contrib import admin
from modeltranslation.admin import TranslationAdmin
from modeltranslation.translator import TranslationOptions, register

from catalog.models import Categories
from project.djnago_admin.admin import ProductModelAdmin


@register(Categories)
class CategoriesTranslationOptions(TranslationOptions):
    fields = ('title', 'alt')


@admin.register(Categories)
class CategoriesAdmin(ProductModelAdmin, TranslationAdmin):
    list_display = ('id', 'title', 'parent', 'alt', 'favorites', 'show_count_products')
