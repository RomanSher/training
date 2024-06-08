from typing import Dict, List

from ckeditor.widgets import CKEditorWidget
from django.contrib import admin
from django.utils.http import urlencode
from django.urls import reverse
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from django.db import models


class BaseAdminModel(admin.ModelAdmin):

    formfield_overrides = {
        models.TextField: {'widget': CKEditorWidget}
    }

    def get_url_changelist(self, model: models.Model, param: Dict) -> str:
        """
        Возвращает ссылку на список объектов модели по параметрам.
        :param model: Модель.
        :param param: Параметры запроса.
        :return: Строка с URL адресом.
        """
        return reverse('admin:%s_%s_changelist' % (
            model._meta.app_label,
            model._meta.model_name)
        ) + '?' + urlencode(param)

    def get_url_change(self, model: models.Model, args: List) -> str:
        """
        Возвращает ссылку на изменение объекта модели.
        :param model: Модель.
        :param args: Аргументы для запроса.
        :return: Ссылка на изменение объекта модели.
        """
        return reverse('admin:%s_%s_change' % (
            model._meta.app_label,
            model._meta.model_name
        ), args=args)

    def get_link(self, url: str, text: str = '', target: str = '') -> str:
        """
        Возвращает ссылку в html формате.
        :param url: URL адрес ссылки.
        :param text: Текст ссылки.
        :param target: Атрибут target ссылки.
        :return: Ссылка в виде HTML.
        """
        """Возвращает ссылку в html формате"""
        return format_html(f'<a href="{url}" target="{target}">{text}</a>')

    def get_html_bool(self, value: bool) -> str:
        """
        Возвращает цветной текст Да/Нет в html формате.
        :param value: Логическое значение.
        :return: Ссылка в виде HTML.
        """
        if value:
            icon = '/static/admin/img/icon-yes.svg'
        else:
            icon = '/static/admin/img/icon-no.svg'
        return format_html(f'<img src="{icon}">')

    def show_or_bool_false(self, obj: models.Model, attribute_name: str) -> str:
        """
        Возвращает значение атрибута объекта или False в виде HTML.
        :param obj: Модель, у которой нужно получить атрибут.
        :param attribute_name: Название атрибута.
        :return: Если значение атрибута не является пустым, возвращает его значение.
        Иначе возвращает False в виде HTML строки.
        """
        attribute = getattr(obj, attribute_name)
        if not attribute:
            return self.get_html_bool(False)
        return attribute

    def set_red_text(self, text: str) -> None:
        """
        Преобразует текст в красный.
        :param text: Текст, который необходимо изменить.
        :return: Возвращает текст красным цветом.
        """
        return format_html(f'<font color="red">{text}<font>')

    def get_help_text(self) -> str:
        """
        Возвращает список полей по которым ведется поиск в модели.
        :return: Ссылка в виде HTML.
        """
        model = self.model
        verbose_name_list = []
        for field in model._meta.fields:
            if field.attname in self.search_fields:
                verbose_name_list.append(field.verbose_name)
        text = ' - '.join(verbose_name_list)
        return format_html(f'{text}')


class UserModelAdmin(BaseAdminModel):

    def show_user(self, obj) -> str:
        """
        Отображает пользователя и возвращает ссылку на его профиль.
        :param obj: Объект.
        :return: Ссылка на профиль пользователя.
        """
        url = self.get_url_change(obj.user, [obj.user.id])
        return self.get_link(url, obj.user.username)

    show_user.short_description = _('User')
    show_user.allow_tags = True


class OrderModelAdmin(BaseAdminModel):

    def show_order(self, obj) -> str:
        """
        Отображает статус заказа.
        :param obj: Объект.
        :return: Ссылка на заказ.
        """
        url = self.get_url_change(obj.order, [obj.order.id])
        return self.get_link(url, obj.order.get_status_display())

    show_order.short_description = _('Order')
    show_order.allow_tags = True

    def show_count_orders(self, obj) -> str:
        """
        Возвращает количество заказов для пользователя
        и ссылку на них.
        :param obj: Объект.
        :return: Ссылка на заказы.
        """
        param = 'user'
        title = _('Order')
        count = obj.order_set.count()
        if count == 0:
            return self.get_html_bool(False)
        url = self.get_url_changelist(obj.order_set.model, {param: obj.id})
        return self.get_link(url, f'{title} ({count})')

    show_count_orders.short_description = _('Order')


class ProductModelAdmin(BaseAdminModel):

    def show_product(self, obj) -> str:
        """
        Отображает продукт.
        :param obj: Объект.
        :return: Ссылка на продукт.
        """
        url = self.get_url_change(obj.product, [obj.product.id])
        return self.get_link(url, obj.product.title)

    show_product.short_description = _('Product')
    show_product.allow_tags = True

    def show_count_products(self, obj) -> str:
        """
        Возвращает количество продуктов для категории
        и ссылку на них.
        :param obj: Объект.
        :return: Ссылка на продукты.
        """
        param = 'category'
        title = _('Product')
        count = obj.product_set.count()
        if count == 0:
            return self.get_html_bool(False)
        url = self.get_url_changelist(obj.product_set.model, {param: obj.id})
        return self.get_link(url, f'{title} ({count})')

    show_count_products.short_description = _('Product')


class CategoriesModelAdmin(BaseAdminModel):

    def show_category(self, obj) -> str:
        """
        Отображает категорию.
        :param obj: Объект.
        :return: Ссылка на категорию.
        """
        url = self.get_url_change(obj.category, [obj.category.id])
        return self.get_link(url, obj.category.title)

    show_category.short_description = _('Category')
    show_category.allow_tags = True


class ReviewModelAdmin(BaseAdminModel):

    def show_count_reviews(self, obj) -> str:
        """
        Возвращает количество отзывов для продукта
        и ссылку на них.
        :param obj: Объект.
        :return: Ссылка на отзывы.
        """
        param = 'product'
        title = _('Review')
        count = obj.review_set.count()
        if count == 0:
            return self.get_html_bool(False)
        url = self.get_url_changelist(obj.review_set.model, {param: obj.id})
        return self.get_link(url, f'{title} ({count})')

    show_count_reviews.short_description = _('Review')


class SpecificationsModelAdmin(BaseAdminModel):

    def show_count_specifications(self, obj) -> str:
        """
        Возвращает количество характеристик для продукта
        и ссылку на них.
        :param obj: Объект.
        :return: Ссылка на характеристики.
        """
        param = 'product'
        title = _('Specifications')
        count = obj.productspecifications_set.count()
        if count == 0:
            return self.get_html_bool(False)
        url = self.get_url_changelist(obj.productspecifications_set.model, {param: obj.id})
        return self.get_link(url, f'{title} ({count})')

    show_count_specifications.short_description = _('Specifications')


class TagsModelAdmin(BaseAdminModel):

    def show_count_tags(self, obj) -> str:
        """
        Возвращает количество тегов для продукта
        и ссылку на них.
        :param obj: Объект.
        :return: Ссылка на теги.
        """
        param = 'product_set__id'
        title = _('Tags')
        count = obj.tags.count()
        if count == 0:
            return self.get_html_bool(False)
        url = self.get_url_changelist(obj.tags.model, {param: obj.id})
        return self.get_link(url, f'{title} ({count})')

    show_count_tags.short_description = _('Tags')
