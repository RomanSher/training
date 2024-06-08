from multiprocessing.connection import Client

import pytest
from django.urls import reverse

from product.serializers import ProductDetailSerializer, ProductSerializer
from tests.utils import (
    assert_200, get_auth_client, create_product_limited_edition,
    create_product
)


@pytest.mark.django_db
class TestProduct:

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
        self.product_1 = create_product_limited_edition()
        self.product_2 = create_product()
        self.url_1 = reverse('product', kwargs={'pk': self.product_1.id})
        self.url_2 = reverse('product-popular')
        self.url_3 = reverse('product-limited')

    def test_product_detail(self) -> None:
        """
        Проверяет корректность отображения детальной информации о продукте.
        Он отправляет GET запрос к указанному URL и проверяет,
        что в ответе возвращается статус код 200.
        Затем сериализует данные о продукте с помощью ProductDetailSerializer
        и изменяет ссылки на изображения, добавляя к ним префикс "http://testserver".
        После этого происходит сравнение полученных данных с ожидаемыми данными.
        :return: None.
        """
        response = self.client.get(self.url_1, content_type=self.content_type)
        assert_200(response)
        expected_data = ProductDetailSerializer(self.product_1).data
        for image in expected_data['images']:
            image['src'] = 'http://testserver' + image['src']
        assert_200(response)
        assert response.data == expected_data

    def test_product_popular(self) -> None:
        """
        Проверяет корректность отображения популярных продуктов.
        Он отправляет GET запрос к указанному URL и проверяет,
        что в ответе возвращается статус код 200.
        Затем сериализует данные о продукте с помощью ProductSerializer
        и изменяет ссылки на изображения, добавляя к ним префикс "http://testserver".
        После этого происходит сравнение полученных данных с ожидаемыми данными.
        :return: None.
        """
        response = self.client.get(self.url_2, content_type=self.content_type)
        expected_data = ProductSerializer([self.product_1, self.product_2], many=True).data
        assert_200(response)
        for obj in expected_data:
            for image in obj['images']:
                image['src'] = 'http://testserver' + image['src']
        assert response.data == expected_data

    def test_product_limited_edition(self) -> None:
        """
        Проверяет корректность отображения продуктов с ограниченным тиражом.
        Он отправляет GET запрос к указанному URL и проверяет,
        что в ответе возвращается статус код 200.
        Затем сериализует данные о продукте с помощью ProductSerializer
        и изменяет ссылки на изображения, добавляя к ним префикс "http://testserver".
        После этого происходит сравнение полученных данных с ожидаемыми данными.
        :return: None.
        """
        response = self.client.get(self.url_3, content_type=self.content_type)
        assert_200(response)
        data = [product for product in (self.product_1, self.product_2) if product.limited_edition]
        expected_data = ProductSerializer(data, many=True).data
        for obj in expected_data:
            for image in obj['images']:
                image['src'] = 'http://testserver' + image['src']
        assert response.data == expected_data
