from multiprocessing.connection import Client

import pytest
from django.urls import reverse

from tests.product.factories import ProductFactory
from tests.catalog.factories import CategoriesFactory
from tests.utils import (get_auth_client, assert_200)


@pytest.mark.django_db
class TestCategories:

    @pytest.fixture(autouse=True)
    def setup(self, client: Client) -> None:
        """
        Фикстура setup устанавливает начальные данные для тестов.
        Она создает клиент и авторизованного пользователя,
        а также создает родительскую категорию и две подкатегории.
        :param client: Объект, представляющий клиента, который
        используется для взаимодействия с веб-сервером.
        :return: None.
        """
        self.client, self.user = get_auth_client(client)
        self.url = reverse('categories')
        self.root_category = CategoriesFactory.create()
        self.child_category = CategoriesFactory(parent=self.root_category)
        self.child_category_2 = CategoriesFactory(parent=self.root_category)

    def test_categories(self) -> None:
        """
        Проверяет, что подкатегории корректно вложены в категорию.
        :return: None.
        """
        response = self.client.get(self.url, content_type='application/json')
        assert_200(response)
        assert response.data[0]['id'] == self.root_category.id
        assert response.data[0]['title'] == self.root_category.title
        assert response.data[0]['subcategories'][0]['id'] == self.child_category.id
        assert response.data[0]['subcategories'][0]['title'] == self.child_category.title
        assert response.data[0]['subcategories'][1]['id'] == self.child_category_2.id
        assert response.data[0]['subcategories'][1]['title'] == self.child_category_2.title
        assert_200(response)


@pytest.mark.django_db
class TestCatalog:

    @pytest.fixture(autouse=True)
    def setup(self, client: Client) -> None:
        """
        Фикстура setup устанавливает начальные данные для тестов.
        Она создает клиент и авторизованного пользователя,
        а также создает два продукта с разными свойствами
        (название, цена, количество, возможность бесплатной доставки)
        и категорию для этих продуктов.
        :param client: Объект, представляющий клиента, который
        используется для взаимодействия с веб-сервером.
        :return: None.
        """
        self.client, self.user = get_auth_client(client)
        self.url = reverse('catalog')
        self.category = CategoriesFactory.create()
        self.product_1 = ProductFactory.create(
            category=self.category,
            title='Product 1',
            price=10,
            count=5,
            free_delivery=True
        )
        self.product_2 = ProductFactory.create(
            category=self.category,
            title='Product 2',
            price=20,
            count=0,
            free_delivery=False
        )

    def test_sorting_by_id(self) -> None:
        """
        Проверяет сортировку продуктов по их идентификатору в убывающем порядке.
        Ожидается, что первым в списке будет продукт с id равным self.product_2.id,
        а вторым - self.product_1.id.
        :return: None.
        """
        response = self.client.get(self.url + '?sort=id&sort_type=inc')
        assert_200(response)
        assert len(response.data['items']) == 2
        assert response.data['items'][0]['id'] == self.product_2.id
        assert response.data['items'][1]['id'] == self.product_1.id

    def test_sorting_by_price(self) -> None:
        """
        Проверяет сортировку продуктов по их цене в убывающем порядке.
        Ожидается, что первым в списке будет продукт с ценой равной self.product_1.price,
        а вторым - self.product_2.price.
        :return: None.
        """
        response = self.client.get(self.url + '?sort=price&sortType=dec')
        assert_200(response)
        assert len(response.data['items']) == 2
        assert response.data['items'][0]['price'] == self.product_1.price
        assert response.data['items'][1]['price'] == self.product_2.price

    def test_filtering_by_available_products(self) -> None:
        """
        Проверяет фильтрацию продуктов по доступности.
        Ожидается, что в списке будут только доступные продукты,
        то есть продукт с id равным self.product_1.id.
        :return: None.
        """
        response = self.client.get(self.url + '?available=True')
        assert_200(response)
        assert len(response.data['items']) == 1
        assert response.data['items'][0]['id'] == self.product_1.id

    def test_filtering_by_free_delivery_products(self) -> None:
        """
        Проверяет фильтрацию продуктов по возможности бесплатной доставки.
        Ожидается, что в списке будут только продукты с возможностью бесплатной доставки,
        то есть продукт с id равным self.product_1.id.
        :return: None
        """
        response = self.client.get(self.url + '?free_delivery=True')
        assert_200(response)
        assert len(response.data['items']) == 1
        assert response.data['items'][0]['id'] == self.product_1.id

    def test_filtering_by_title(self) -> None:
        """
        Проверяет фильтрацию продуктов по названию.
        Ожидается, что в списке будет только продукт с названием 'Product 1',
        то есть продукт с id равным self.product_1.id.
        :return: None.
        """
        response = self.client.get(self.url + '?name=Product 1')
        assert_200(response)
        assert len(response.data['items']) == 1
        assert response.data['items'][0]['id'] == self.product_1.id

    def test_filtering_by_minimum_price(self) -> None:
        """
        Проверяет фильтрацию продуктов по минимальной цене.
        Ожидается, что в списке будет только продукт с ценой больше 15,
        то есть продукт с id равным self.product_2.id.
        :return: None.
        """
        response = self.client.get(self.url + '?min_price=15')
        assert_200(response)
        assert len(response.data['items']) == 1
        assert response.data['items'][0]['id'] == self.product_2.id

    def test_filtering_by_maximum_price(self) -> None:
        """
        Проверяет фильтрацию продуктов по максимальной цене.
        Ожидается, что в списке будет только продукт с ценой меньше 15,
        то есть продукт с id равным self.product_1.id.
        :return: None.
        """
        response = self.client.get(self.url + '?max_price=15')
        assert_200(response)
        assert len(response.data['items']) == 1
        assert response.data['items'][0]['id'] == self.product_1.id
