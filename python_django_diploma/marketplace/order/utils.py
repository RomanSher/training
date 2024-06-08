from typing import List, Tuple, Any, Dict

from django.contrib.sessions.backends.base import SessionBase
from django.db.models import F

from basket.models import Basket
from order.models import Order, OrderCountProduct
from product.models import Product
from project import settings
from project.exceptions import OrderAvailabilityError, OrderProductNotFoundError
from user.models import User


class ProcessingOrderCreation:

    def __init__(self, data: Dict, user: User, session: SessionBase) -> None:
        """
        Инициализирует объект заказа с указанными данными.
        :param data: Словарь с данными, необходимыми для создания заказа.
        :param user: Пользователь, для которого необходимо создать заказ.
        :param session: Сессия клиента.
        :return: None.
        """
        self.data = data
        self.user = user
        self.session = session

    def getting_the_required_fields(self) -> List[Tuple[Any, Any, Any]]:
        """
        Метод для получения необходимых полей из data.
        :return: Список с кортежами, содержащими информацию о продуктах в заказе.
        Каждый кортеж содержит id продукта, количество и цену.
        """
        products_in_order = [
            (obj['id'], obj['count'], obj['price']) for obj in self.data
        ]
        return products_in_order

    def total_cost(self) -> int:
        """
        Метод для получения общей стоимости заказа.
        :return: Общая стоимость заказа.
        """

        total_sum = sum(int(obj['price']) * int(obj['count']) for obj in self.data)
        return total_sum

    def creating_an_order(self) -> Order:
        """
        Метод для создания заказа для авторизованного и
        неавторизованного пользователя.
        :return: Созданный заказ.
        """
        if self.user.is_authenticated:
            order = Order.objects.create(
                user_id=self.user.id,
                total_cost=self.total_cost(),
                full_name=self.user.full_name if self.user.full_name else None,
                email=self.user.email if self.user.email else None,
                phone=self.user.phone if self.user.phone else None,
            )
        else:
            order = Order.objects.create(
                total_cost=self.total_cost()
            )
        self.filling_in_the_quantity_of_products(order)

        return order

    def filling_in_the_quantity_of_products(self, order: Order) -> None:
        """
        Метод для создания количества заказанных продуктов.
        :param order: Созданный заказ.
        :return: None.
        """
        order_count_products = []
        updated_products = []
        for product_id, count, price in self.getting_the_required_fields():
            self.product_availability(product_id, count)
            order_count_products.append(
                OrderCountProduct(
                    product_id=product_id,
                    order=order,
                    count=count,
                    price=price
                )
            )
            updated_products.append(
                Product(
                    id=product_id,
                    count=F('count') - count
                )
            )
        Product.objects.bulk_update(updated_products, ['count'])
        OrderCountProduct.objects.bulk_create(order_count_products)
        self.clear_basket()

    def clear_basket(self) -> None:
        """
        Очищает корзину после создания заказа.
        :return: None.
        """
        if self.user.is_authenticated:
            Basket.objects.filter(user=self.user).delete()
        else:
            self.session[settings.CART_SESSION_ID] = {}

    @staticmethod
    def product_availability(product_id: int, count: int) -> None:
        """
        Возвращает исключение, если запрашиваемое количество товара
        недоступно для заказа или товар не найден.
        :param product_id: Идентификатор продукта.
        :param count: Количество товаров для заказа.
        :return: None.
        """
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            raise OrderProductNotFoundError

        if product.count < count:
            raise OrderAvailabilityError
