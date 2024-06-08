from multiprocessing.connection import Client

import pytest
from django.urls import reverse

from tests.basket.factories import BasketFactory
from tests.utils import (
    get_auth_client, assert_200, create_basket, create_product,
    session_init, session_save, add_product_session, get_cart
)


@pytest.mark.django_db
class TestAuthUserBasket:

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
        self.session, self.cart = session_init(client)
        self.url = reverse('basket')
        self.product_1 = create_product()
        self.product_2 = create_product()

    def test_get_basket(self) -> None:
        """
        Создает корзину с продуктом для пользователя и проверяет, что
        данные в корзине возвращаются в правильном формате.
        :return: None.
        """
        basket = create_basket(user=self.user, product=self.product_1)
        response = self.client.get(self.url)
        assert_200(response)
        assert response.data[0]['id'] == basket.id
        assert response.data[0]['count'] == basket.count
        assert response.data[0]['price'] == basket.price

    def test_association_basket(self) -> None:
        """
        Тестируется функционал связывания корзины пользователя и корзины сессии.
        Сначала создается корзина для авторизованного пользователя и добавляется
        в нее продукт. Затем создается сессия и в нее добавляется self.product_2.
        После отправки запроса, ожидается объединение двух корзин.
        :return: None.
        """
        basket = create_basket(user=self.user, product=self.product_1)
        assert BasketFactory._meta.model.objects.all().count() == 1
        self.adding_product_to_session()
        response = self.client.get(self.url)
        assert_200(response)
        assert BasketFactory._meta.model.objects.all().count() == 2
        assert response.data[0]['id'] == 3
        assert response.data[0]['count'] == basket.count
        assert response.data[0]['price'] == basket.price
        assert response.data[1]['id'] == 4
        assert response.data[1]['count'] == 2

    def test_increase_in_quantity_in_basket(self) -> None:
        """
        Проверяет, что после запроса на добавление,
        количество товаров в корзине увеличивается на указанное значение.
        Сначала создается корзина с продуктом, затем отправляется запрос
        на увеличение количества товара в корзине. После этого проверяется,
        что количество товаров в корзине увеличилось на указанное значение.
        :return: None.
        """
        basket_factory = create_basket(user=self.user, product=self.product_1)
        data = {'id': self.product_1.id, 'count': 2}
        assert BasketFactory._meta.model.objects.all().count() == 1
        response = self.client.post(self.url, data, content_type=self.content_type)
        assert_200(response)
        assert BasketFactory._meta.model.objects.all().count() == 1
        basket = BasketFactory._meta.model.objects.filter(user=self.user).first()
        assert basket.product_id == self.product_1.id
        assert basket.count == basket_factory.count + 2

    def test_adding_product_to_basket(self) -> None:
        """
        Проверяет, что после запроса на добавление продукта в корзину,
        количество продуктов в корзине увеличивается на указанное значение.
        Сначала создается корзина с продуктом, затем отправляется запрос
        на добавление продукта в корзину. После этого проверяется,
        что количество продуктов увеличилось на указанное значение.
        :return: None.
        """
        self.test_increase_in_quantity_in_basket()
        data = {'id': self.product_2.id, 'count': 1}
        response = self.client.post(self.url, data, content_type=self.content_type)
        assert_200(response)
        assert BasketFactory._meta.model.objects.all().count() == 2
        basket = BasketFactory._meta.model.objects.filter(user=self.user).last()
        assert basket.product_id == self.product_2.id
        assert basket.price == self.product_2.price
        assert basket.count == 1

    def test_reduce_basket(self) -> None:
        """
        Проверяет, что после запроса на уменьшение,
        количество товаров в корзине уменьшается на указанное значение.
        Сначала создается корзина с продуктом, затем отправляется запрос
        на уменьшение количества товара в корзине. После этого проверяется,
        что количество товаров в корзине уменьшилось на указанное значение.
        :return: None.
        """
        basket_factory = create_basket(user=self.user, product=self.product_1)
        data = {'id': self.product_1.id, 'count': 1}
        response = self.client.delete(self.url, data, content_type=self.content_type)
        assert_200(response)
        basket = BasketFactory._meta.model.objects.filter(user=self.user).last()
        assert basket_factory.id == basket.id
        assert basket_factory.count - 1 == basket.count

    def test_delete_product_in_basket(self) -> None:
        """
        Проверяет, что товар удаляется из корзины после запроса на уменьшение
        количества товара, когда количество товара в корзине становится меньше 1.
        Сначала создает корзину с продуктом, затем отправляем запрос на уменьшение
        количества товара. После этого проверяет, что товар был успешно удален из
        корзины.
        :return: None.
        """
        basket_factory = create_basket(user=self.user, product=self.product_1)
        assert BasketFactory._meta.model.objects.all().count() == 1
        data = {'id': self.product_1.id, 'count': basket_factory.count}
        response = self.client.delete(self.url, data, content_type=self.content_type)
        assert_200(response)
        basket = BasketFactory._meta.model.objects.filter(user=self.user)
        assert list(basket) == []

    def adding_product_to_session(self) -> None:
        """
        Добавляет товар в сессию.
        В сессию добавляется продукт product_1 в количестве 2 товаров.
        После этого сессия сохраняется.
        :return: None.
        """
        add_product_session(self.cart, self.product_2, 2)
        session_save(self.session, self.cart)


@pytest.mark.django_db
class TestBasket:

    @pytest.fixture(autouse=True)
    def setup(self, client: Client) -> None:
        """
        Фикстура setup устанавливает начальные данные для тестов.
        Создает клиент и инициализирует сессию,
        а также создает два продукта с разными свойствами.
        :param client: Объект, представляющий клиента, который
        используется для взаимодействия с веб-сервером.
        :return: None.
        """
        self.content_type = 'application/json'
        self.client = client
        self.session, self.cart = session_init(client)
        self.url = reverse('basket')
        self.product_1 = create_product()
        self.product_2 = create_product()

    def test_get_cart(self):
        """
        Добавляет продукт в сессию неавторизованного пользователя и проверяет,
        что данные в корзине возвращаются в правильном формате.
        :return: None.
        """
        self.adding_product_to_session()
        product_count = self.cart.get(str(self.product_1.id), {}).get('count', 0)
        product_price = self.cart.get(str(self.product_1.id), {}).get('price', 0)
        assert product_count == 2
        response = self.client.get(self.url, content_type=self.content_type)
        assert_200(response)
        assert response.data[0]['id'] == self.product_1.id
        assert response.data[0]['count'] == product_count
        assert response.data[0]['price'] == product_price

    def test_adding_product_to_cart(self):
        """
        Проверяет, что товар добавляется в корзину.
        Сначала отправляется запрос на добавление товара в корзину.
        После этого проверяется, что количество товаров в корзине увеличилось
        на указанное значение.
        :return: None.
        """
        data = {'id': self.product_1.id, 'count': 3}
        response = self.client.post(self.url, data, content_type=self.content_type)
        assert_200(response)
        cart = get_cart(self.client)
        session_product_key = list(cart.keys())
        session_product_count = cart.get(str(session_product_key[0]), {}).get('count', 0)
        session_product_price = cart.get(str(session_product_key[0]), {}).get('price', 0)
        assert int(session_product_key[0]) == self.product_1.id
        assert int(session_product_count) == 3
        assert int(session_product_price) == self.product_1.price

    def test_adding_two_product_to_cart(self):
        """
        Проверяет, что товары добавляются в корзину и соответствуют указанному количеству.
        Сначала добавляется один продукт в корзину, после чего проверяет,
        что количество товаров в корзине увеличилось на указанное значение.
        Затем отправляется запрос на добавление второго продукта в корзину и
        проверяет, что количество продуктов соответствуют указанному количеству.
        :return: None.
        """
        self.test_adding_product_to_cart()
        data = {'id': self.product_2.id, 'count': 1}
        response = self.client.post(self.url, data, content_type=self.content_type)
        assert_200(response)
        cart = get_cart(self.client)
        session_product_keys = list(cart.keys())
        session_product_1_count = cart.get(str(session_product_keys[0]), {}).get('count', 0)
        session_product_1_price = cart.get(str(session_product_keys[0]), {}).get('price', 0)
        session_product_2_count = cart.get(str(session_product_keys[1]), {}).get('count', 0)
        session_product_2_price = cart.get(str(session_product_keys[1]), {}).get('price', 0)
        assert int(session_product_keys[0]) == self.product_1.id
        assert int(session_product_1_price) == self.product_1.price
        assert int(session_product_1_count) == 3
        assert int(session_product_keys[1]) == self.product_2.id
        assert int(session_product_2_price) == self.product_2.price
        assert int(session_product_2_count) == 1

    def test_reduce_card(self):
        """
        Проверяет, что после запроса на уменьшение,
        количество товаров в корзине уменьшается на указанное значение.
        Сначала создается корзина с продуктом, затем отправляется запрос
        на уменьшение количества товара в корзине. После этого проверяется,
        что количество товаров в корзине уменьшилось на указанное значение.
        :return: None.
        """
        self.adding_product_to_session()
        data = {'id': self.product_1.id, 'count': 1}
        response = self.client.delete(self.url, data, content_type=self.content_type)
        assert_200(response)
        cart = get_cart(self.client)
        session_product_keys = list(cart.keys())
        session_product_1_count = cart.get(str(session_product_keys[0]), {}).get('count', 0)
        session_product_1_price = cart.get(str(session_product_keys[0]), {}).get('price', 0)
        assert int(session_product_keys[0]) == self.product_1.id
        assert int(session_product_1_price) == self.product_1.price
        assert int(session_product_1_count) == 1

    def test_delete_product_in_cart(self):
        """
        Проверяет, что товар удаляется из корзины после запроса на уменьшение
        количества товара, когда количество товара в корзине становится меньше 1.
        Сначала создает корзину с продуктом, затем отправляем запрос на уменьшение
        количества товара. После этого проверяет, что товар был успешно удален из корзины.
        :return: None.
        """
        self.test_reduce_card()
        data = {'id': self.product_1.id, 'count': self.product_1.count - 1}
        response = self.client.delete(self.url, data,  content_type=self.content_type)
        assert_200(response)
        cart = get_cart(self.client)
        session_product_keys = list(cart.keys())
        assert session_product_keys == []

    def adding_product_to_session(self) -> None:
        """
        Добавляет товар в сессию и сохраняет её.
        В сессию добавляется продукт product_1 в количестве 2 товаров.
        После этого сессия сохраняется.
        :return: None.
        """
        add_product_session(self.cart, self.product_1, 2)
        session_save(self.session, self.cart)
