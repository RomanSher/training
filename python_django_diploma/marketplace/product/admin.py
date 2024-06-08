from django.contrib import admin
from modeltranslation.admin import TranslationAdmin
from modeltranslation.translator import TranslationOptions, register
from rangefilter.filters import NumericRangeFilter, DateRangeFilter

from product.models import (
    ProductImage, Product, Tag,
    Review, ProductSpecifications, Sale
)
from project.djnago_admin.admin import (
    ProductModelAdmin, ReviewModelAdmin, SpecificationsModelAdmin,
    CategoriesModelAdmin, TagsModelAdmin
)
from project.djnago_admin.filters import MinRateFilter, MaxRateFilter


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    list_display = ('id', 'product', 'alt')


class ProductSpecificationsInline(admin.TabularInline):
    model = ProductSpecifications
    list_display = ('name', 'value', 'product')


@register(Product)
class ProductTranslationOptions(TranslationOptions):
    fields = ('title', 'description', 'full_description')


@register(ProductImage)
class ProductImageTranslationOptions(TranslationOptions):
    fields = ('alt',)


@register(Tag)
class TagTranslationOptions(TranslationOptions):
    fields = ('name',)


@register(ProductSpecifications)
class ProductSpecificationsTranslationOptions(TranslationOptions):
    fields = ('name', 'value')


@admin.register(Product)
class ProductAdmin(
    CategoriesModelAdmin,
    ReviewModelAdmin,
    SpecificationsModelAdmin,
    TagsModelAdmin,
    TranslationAdmin
):
    list_display = (
        'id', 'title', 'price', 'count', 'show_category',
        'free_delivery', 'limited_edition', 'show_count_reviews',
        'rating', 'show_count_specifications', 'show_count_tags'
    )
    search_fields = ('id', 'title', 'category__title')
    list_filter = (('price', NumericRangeFilter),)
    inlines = [ProductImageInline, ProductSpecificationsInline]


@admin.register(ProductImage)
class ProductImageAdmin(ProductModelAdmin, TranslationAdmin):
    model = ProductImage
    list_display = ('id', 'show_product', 'alt')
    search_fields = ('id', 'alt', 'product_id', 'product__title')


@admin.register(Sale)
class SaleAdmin(ProductModelAdmin):
    list_display = ('id', 'show_product', 'sale_price', 'date_from', 'date_to')
    search_fields = ('id', 'product_id', 'product__title')
    list_filter = (
        ('date_from', DateRangeFilter),
        ('date_to', DateRangeFilter)
    )


@admin.register(Tag)
class TagAdmin(TranslationAdmin):
    list_display = ('id', 'name')
    search_fields = ('id', 'name')


@admin.register(Review)
class ReviewAdmin(ProductModelAdmin):
    list_display = ('id', 'author', 'email', 'show_product', 'rate')
    search_fields = ('id', 'name', 'email', 'product_id', 'product__title')
    list_filter = (MinRateFilter, MaxRateFilter)


@admin.register(ProductSpecifications)
class ProductSpecificationsAdmin(ProductModelAdmin, TranslationAdmin):
    list_display = ('id', 'name', 'value', 'show_product')
    search_fields = ('id', 'name', 'product_id', 'product__title')
