from typing import List

from django.db.models import QuerySet
from django_filters import rest_framework as filters
from product.models import Product


class TagsFilter(filters.BaseInFilter, filters.NumberFilter):

    def filter(self, queryset: QuerySet, value: List) -> QuerySet:
        """
        Фильтрует queryset по тегу.
        :param queryset: QuerySet - исходный набор данных.
        :param value: Список идентификаторов тегов.
        :return: Отфильтрованный набор данных.
        """
        if value:
            return queryset.filter(tags__id__in=value)
        return queryset


class CatalogRequestFilter(filters.FilterSet):
    available = filters.BooleanFilter(method='filter_available')
    free_delivery = filters.BooleanFilter(method='filter_free_delivery')
    name = filters.CharFilter(field_name='title', lookup_expr='icontains')
    min_price = filters.NumberFilter(field_name='price', lookup_expr='gte')
    max_price = filters.NumberFilter(field_name='price', lookup_expr='lte')
    tags = TagsFilter(field_name='tags', lookup_expr='in')

    class Meta:
        model = Product
        fields = ['count', 'free_delivery', 'available', 'title', 'price', 'tags']

    def filter_available(self, queryset: QuerySet, name: str, value: int) -> QuerySet:
        """
        Фильтрует queryset по наличию товаров.
        :param queryset: QuerySet - исходный набор данных.
        :param name: Имя фильтра.
        :param value: Значение фильтра (True - товары в наличии, False - все товары).
        :return: Отфильтрованный набор данных.
        """
        if value:
            return queryset.filter(count__gt=0)
        return queryset

    def filter_free_delivery(self, queryset: QuerySet, name: str, value: bool) -> QuerySet:
        """
        Фильтрует queryset по бесплатной доставке.
        :param queryset: QuerySet - исходный набор данных.
        :param name: Имя фильтра.
        :param value: Значение фильтра (True - бесплатная доставка, False - все товары).
        :return: Отфильтрованный набор данных.
        """
        if value:
            return queryset.filter(free_delivery=True)
        return queryset
