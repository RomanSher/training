from django.conf import settings
from django.db.models import QuerySet, F
from rest_framework.request import Request

from product.models import Product
from basket.models import Basket
from django.db import transaction

from project.exceptions import (
    BasketProductNotFoundError, BasketAddProductError,
    BasketNotEnoughError, BasketUpdatingProductError
)


class Cart:
    def __init__(self, request: Request) -> None:
        """
        Инициализирует корзину.
        :param request: Объект запроса.
        """
        self.product_id = request.data.get('id', None)
        self.product_count = request.data.get('count', None)
        self.session = request.session
        self.cart = self.session.get(settings.CART_SESSION_ID)
        self.user = request.user
        self.update_basket_items()

    @transaction.atomic
    def update_basket_items(self) -> None:
        """
        Проверяет содержимое корзины и объединяет корзины при авторизации.
        :return: None.
        """
        if self.user.is_authenticated and self.cart:
            product_ids = self.cart.keys()
            for product_id in product_ids:
                basket_item, created = Basket.objects.get_or_create(
                    product_id=product_id,
                    user_id=self.user.id
                )
                count = self.cart[product_id]['count']
                product = Product.objects.filter(id=product_id).first()

                if self.checking_product_availability_for_authenticated_user(product, count):
                    basket_item.count += count

                else:
                    basket_item.count = product.count

                basket_item.price = self.cart[product_id]['price']
                basket_item.save()
            self.session['cart'] = {}
        elif not self.cart:
            self.cart = self.session[settings.CART_SESSION_ID] = {}

    def store_products_in_cart(self) -> QuerySet[Product]:
        """
        Перебор элементов в корзине и получение продуктов из базы данных.
        :return: QuerySet[Product].
        """
        if self.user.is_authenticated:
            product_ids = Basket.objects.filter(user_id=self.user.id).values_list('product_id')
        else:
            product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        return products

    def save(self) -> None:
        """
        Сохраняет изменения в корзине.
        :return: None.
        """
        self.session[settings.CART_SESSION_ID] = self.cart
        self.session.modified = True

    @transaction.atomic
    def add_product_or_update(self) -> None:
        """
        Добавляет продукт в корзину или обновляет его количество и цену.
        :return: None.
        """
        try:
            product = Product.objects.get(id=self.product_id)

            if isinstance(self.product_count, int):

                if self.user.is_authenticated:

                    if self.checking_product_availability_for_authenticated_user(product, self.product_count):
                        self.add_product_or_update_for_authenticated_user(product)
                    else:
                        raise BasketNotEnoughError
                else:

                    if self.checking_product_availability_for_anonym_user(product, self.product_count):
                        self.add_product_or_update_for_anonym_user(product)
                    else:
                        raise BasketNotEnoughError
                return

            else:
                raise BasketAddProductError

        except Product.DoesNotExist:
            raise BasketProductNotFoundError

    def add_product_or_update_for_authenticated_user(self, product: Product) -> None:
        """
        Добавляет или обновляет продукт в корзине для авторизованного пользователя.
        :param product: Экземпляр Product, который необходимо добавить или обновить.
        :return: None.
        """
        basket, created = Basket.objects.get_or_create(
            product_id=self.product_id,
            user_id=self.user.id,
            defaults={
                'price': product.price,
                'count': self.product_count
            }
        )
        if not created:
            basket.count = F('count') + self.product_count
            basket.save(update_fields=['count', 'price'])

    def add_product_or_update_for_anonym_user(self, product: Product) -> None:
        """
        Добавляет или обновляет продукт в корзине для неавторизованного пользователя.
        :param product: Экземпляр Product, который необходимо добавить или обновить.
        :return: None.
        """
        self.cart.setdefault(str(product.id), {'count': 0, 'price': str(product.price)})
        self.cart[str(product.id)]['count'] += self.product_count
        self.save()

    def checking_product_availability_for_authenticated_user(self, product: Product, count: int) -> bool:
        """
        Проверяет доступность продукта для авторизованного пользователя.
        :param product: Экземпляр Product, для которого нужно проверить доступность.
        :param count: Количество продукта.
        :return: True, если продукт доступен, False - в противном случае.
        """
        product_in_basket = Basket.objects.filter(
            product=product,
            user_id=self.user.id
        ).values('count').first()
        product_count = product_in_basket['count'] if product_in_basket else 0
        return product.count >= product_count + count

    def checking_product_availability_for_anonym_user(self, product: Product, count: int) -> bool:
        """
        Проверяет доступность продукта для неавторизованного пользователя.
        :param product: Экземпляр Product, для которого нужно проверить доступность.
        :param count: Количество продукта.
        :return: True, если продукт доступен, False - в противном случае.
        """
        cart_item = self.cart.get(str(product.id), None)

        if cart_item is None:
            count_product_in_basket = count

        else:
            count_product_in_basket = cart_item.get('count', 0) + count

        return product.count >= count_product_in_basket

    def reduce_product_or_update(self) -> None:
        """
        Убирает продукт из корзины или обновляет его количество.
        :return: None.
        """
        if isinstance(self.product_count, int):

            if self.user.is_authenticated:
                self.reduce_product_or_update_for_authenticated_user()

            else:
                self.reduce_product_or_update_for_anonym_user()

        else:
            raise BasketUpdatingProductError

    def reduce_product_or_update_for_authenticated_user(self) -> None:
        """
        Удаляет или обновляет продукт в корзине для авторизованного пользователя.
        :return: None.
        """
        Basket.objects.filter(
            product_id=self.product_id,
            user_id=self.user.id
        ).update(count=F('count') - int(self.product_count))
        Basket.objects.filter(
            count__lte=0,
            product_id=self.product_id,
            user_id=self.user.id
        ).delete()

    def reduce_product_or_update_for_anonym_user(self) -> None:
        """
        Удаляет или обновляет продукт в корзине для неавторизованного пользователя.
        :return: None.
        """
        cart_item = self.cart.get(str(self.product_id))

        if cart_item:
            count = int(self.product_count)
            if int(cart_item['count']) > count:
                cart_item['count'] -= count
                self.save()
            else:
                del self.cart[str(self.product_id)]
                self.save()

    def count_product_in_basket(self, product_id: str) -> int:
        """
        Получает количество продуктов.
        :param product_id: Идентификатор продукта для которого нужно получить количество.
        :return: Количество продуктов.
        """
        if self.user.is_authenticated:
            product = Basket.objects.filter(
                product_id=product_id,
                user_id=self.user.id
            ).values_list('count', flat=True).first() or 0
            return product
        else:
            return self.cart.get(product_id, {}).get('count', 0)

    def price_product_in_basket(self, product_id: str) -> int:
        """
        Получает цену за продукт.
        :param product_id: Идентификатор продукта для которого нужно получить количество.
        :return: Цена за продукт.
        """
        if self.user.is_authenticated:
            product = Basket.objects.filter(
                product_id=product_id,
                user_id=self.user.id
            ).values_list('price', flat=True).first() or 0
            return product
        else:
            return self.cart.get(product_id, {}).get('price', 0)
