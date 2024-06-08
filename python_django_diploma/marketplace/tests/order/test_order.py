from multiprocessing.connection import Client

import pytest
from django.urls import reverse

from tests.order.factories import OrderFactory
from product.serializers import ProductSerializer
from tests.utils import (
    assert_200, get_auth_client, create_product, create_order,
    create_payment_transaction, assert_201
)


@pytest.mark.django_db
class TestOrder:

    @pytest.fixture(autouse=True)
    def setup(self, client: Client) -> None:
        """
        Фикстура setup устанавливает начальные данные для тестов.
        Она создает клиент и авторизованного пользователя,
        а также создает два продукта с разными свойствами.
        :param client: Объект, представляющий клиента, который
        используется для взаимодействия с веб-сервером.
        :return: None.
        """
        self.content_type = 'application/json'
        self.client, self.user = get_auth_client(client)
        self.product_1 = create_product()
        self.product_2 = create_product()
        self.url_1 = reverse('orders')

    def test_get_order(self) -> None:
        """
        Проверяет корректность отображения заказа.
        Отправляет GET запрос к указанному URL и проверяет,
        что в ответе возвращается статус код 200.
        :return: None.
        """
        order = create_order(user=self.user, product=self.product_1)
        response = self.client.get(self.url_1, content_type=self.content_type)
        assert_200(response)
        assert response.data[0]['id'] == order.id
        assert response.data[0]['full_name'] == order.full_name
        assert response.data[0]['email'] == order.email
        assert response.data[0]['phone'] == order.phone
        assert response.data[0]['total_cost'] == order.total_cost
        assert response.data[0]['status'] == order.status
        assert response.data[0]['city'] == order.city
        assert response.data[0]['address'] == order.address
        assert response.data[0]['products'][0]['id'] == order.products.first().id

    def test_create_order(self) -> None:
        """
        Проверяет создание заказа.
        Создает данные для заказа и отправляем POST-запрос на сервер.
        Проверяет количество заказов до и после запроса и общую
        стоимость созданного заказа.
        :return: None.
        """
        data = [
            {'id': self.product_1.id, 'count': 2, 'price': self.product_1.price},
            {'id': self.product_2.id, 'count': 1, 'price': self.product_2.price},
        ]
        assert OrderFactory._meta.model.objects.count() == 0
        response = self.client.post(self.url_1, data, content_type=self.content_type)
        assert_200(response)
        assert OrderFactory._meta.model.objects.count() == 1
        order = OrderFactory._meta.model.objects.get(id=response.data.get('id'))
        assert order.total_cost == sum(obj['price'] * obj['count'] for obj in data)

    def test_update_order(self) -> None:
        """
        Тест проверяет возможность обновления данных заказа.
        В тесте создается заказ с продуктом, затем изменяются данные заказа
        (город, адрес, имя, телефон) и через PATCH запрос обновляются на сервере.
        Проверяется корректность обновленных данных, соответствие полей заказа
        и данных из ответа сервера.
        :return: None.
        """
        serializer = ProductSerializer(self.product_1)
        order = create_order(user=self.user, product=self.product_1)

        changed_city = 'Washington'
        changed_address = '1125 16th Street'
        changed_full_name = 'Ivanov Ivan'
        changed_phone = '+79995553322'

        data = {
            'id': order.id, 'created_at': order.created_at, 'full_name': changed_full_name,
            'email': order.email, 'phone': changed_phone, 'delivery_type': order.delivery_type,
            'payment_type': order.payment_type, 'total_cost': order.total_cost,
            'status': order.status, 'city': changed_city, 'address': changed_address,
            'products': serializer.data
        }

        url = reverse('orders-detail',  kwargs={'pk': order.id})
        response = self.client.patch(url, data, content_type=self.content_type)
        assert_200(response)
        assert response.data['id'] == order.id
        assert response.data['full_name'] == changed_full_name
        assert response.data['email'] == order.email
        assert response.data['phone'] == changed_phone
        assert response.data['delivery_type'] == order.delivery_type
        assert response.data['payment_type'] == order.payment_type
        assert response.data['address'] == changed_address
        assert response.data['city'] == changed_city

    def test_payment_transaction(self) -> None:
        """
        Проверяет процесс выполнения транзакции оплаты.
        Если номер карты заканчивается на четную цифру,
        то ожидается ответ 201, в противном случае - ожидается ответ 400.
        :return: None.
        """
        pt = create_payment_transaction(self.user)
        url = reverse('payment', kwargs={'pk': pt.id})
        data = {
            'code': '222',
            'month': '12',
            'name': 'Ivanov Ivan',
            'number': '111122223333444',
            'year': '25'
        }
        response = self.client.post(url, data, content_type=self.content_type)
        assert_201(response)
