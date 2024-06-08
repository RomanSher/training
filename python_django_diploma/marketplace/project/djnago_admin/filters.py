from typing import List, Tuple

from django.contrib import admin
from django.db import models
from django.db.models import QuerySet
from django.utils.translation import gettext_lazy as _
from rest_framework.request import Request


class MinRateFilter(admin.SimpleListFilter):
    title = _('Min Rate')
    parameter_name = _('min_rate')

    def lookups(self, request: Request, model_admin: models.Model) -> List[Tuple[str, str]]:
        """
        Возвращает список значений для фильтрации по максимальной оценке.
        :param request: Объект запроса.
        :param model_admin:
        :return: Список значений.
        """
        return [(str(num), str(num)) for num in range(11)]

    def queryset(self, request: Request, queryset: QuerySet) -> QuerySet:
        """
        Применяет фильтрацию по минимальной оценке к queryset.
        :param request: Объект запроса.
        :param queryset: QuerySet.
        :return: QuerySet.
        """
        value = self.value()
        if value is not None:
            return queryset.filter(rate__gte=int(value))


class MaxRateFilter(admin.SimpleListFilter):
    title = _('Max Rate')
    parameter_name = _('max_rate')

    def lookups(self, request: Request, model_admin: models.Model) -> List[Tuple[str, str]]:
        """
        Возвращает список значений для фильтрации по минимальной оценке.
        :param request: Объект запроса.
        :param model_admin:
        :return: Список значений.
        """
        return [(str(num), str(num)) for num in range(11)]

    def queryset(self, request: Request, queryset: QuerySet) -> QuerySet:
        """
        Применяет фильтрацию по максимальной оценке к queryset.
        :param request: Объект запроса.
        :param queryset: QuerySet.
        :return: QuerySet.
        """
        value = self.value()
        if value is not None:
            return queryset.filter(rate__lte=int(value))
