from multiprocessing.connection import Client
from types import SimpleNamespace
from typing import Tuple, Dict, Union

from django.contrib.sessions.backends.base import SessionBase
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from basket.models import Basket
from order.models import Order, PaymentTransaction
from product.models import Product, Review, Sale, Tag
from project import settings
from tests.basket.factories import BasketFactory
from tests.order.factories import (
    OrderFactory, OrderCountProductFactory, PaymentTransactionFactory
)
from tests.product.factories import (
    CategoriesFactory, ProductFactory, ProductImageFactory, TagFactory,
    ReviewFactory, ProductSpecificationsFactory, SaleFactory
)
from user.models import User


CartData = Dict[str, Dict[str, Union[int, str]]]


def get_auth_client(client: Client) -> Tuple[Client, User]:
    """
    Получает клиентский объект и выполняет аутентификацию
    пользователя, создавая временного тестового пользователя
    и получая токен доступа для этого пользователя.
    :param client: Объект, представляющий клиента, который
    используется для взаимодействия с веб-сервером.
    :return: Кортеж из объекта Client и объекта User.
    """
    url = reverse('token')
    data = {
        'username': 'Ivanov',
        'password': 'password123'
    }
    user = create_test_user(data['username'], data['password'])
    response = client.post(url, data)
    token = response.json()['access']
    client.defaults['HTTP_AUTHORIZATION'] = f'Bearer {token}'
    client.post(url, content_type='application/json')
    user.refresh_from_db()
    return client, user


def get_auth_client_full(client: Client) -> Tuple[Client, User]:
    """
    Получает клиентский объект и выполняет аутентификацию
    пользователя, создавая временного тестового пользователя
    с полностью заполненными данными и получая токен доступа
    для этого пользователя.
    :param client: Объект, представляющий клиента, который
    используется для взаимодействия с веб-сервером.
    :return: Кортеж из объекта Client и объекта User.
    """
    url = reverse('token')
    avatar_file = SimpleUploadedFile(
        'avatar.jpg',
        b'file_content',
        content_type='image/jpeg'
    )
    data = {
        'username': 'Ivanov',
        'password': 'password123',
        'full_name': 'Ivanov Ivan Ivanovich',
        'email': 'ivanov@example.com',
        'phone': '+79998887766',
        'avatar': avatar_file
    }
    user = create_test_full_user(data)
    response = client.post(url, data)
    token = response.json()['access']
    client.defaults['HTTP_AUTHORIZATION'] = f'Bearer {token}'
    client.post(url, content_type='application/json')
    user.refresh_from_db()
    return client, user


def create_test_user(username: str, password: str) -> 'User':
    """
    Создает тестового пользователя.
    :param username: Имя пользователя.
    :param password: Пароль пользователя.
    :return: Экземпляр User.
    """
    user = User.objects.create_user(
        username=username,
        password=password
    )
    return user


def create_test_full_user(data: Dict) -> 'User':
    """
    Создает тестового пользователя с полными данными.
    :param data: Словарь, содержащий пользовательские данные.
    :return: Экземпляр User.
    """
    user = User.objects.create_user(**data)
    return user


def get_token(user: User) -> Union[AccessToken, None]:
    """
    Возвращает токен доступа для указанного пользователя.
    :param user: Экземпляр User.
    :return: Токен доступа для указанного пользователя или None,
    если токен не найден.
    """
    token = AccessToken.for_user(user)
    return token


def error_msg(response_status: int, expected_status: int) -> str:
    """
    Функция для формирования сообщения об ошибке в случае несовпадения
    ожидаемого и фактического HTTP-статуса.
    :param response_status: Фактический HTTP-статус ответа.
    :param expected_status: Ожидаемый HTTP-статус.
    :return: Сообщение об ошибке.
    """
    return f'Ожидался код: {expected_status}, код ответа: {response_status}'


def assert_method(response: Response, expected_status: int) -> None:
    """
    Функция для проверки соответствия фактического HTTP-статуса ожидаемому.
    :param response: Ответ от сервера.
    :param expected_status: Ожидаемый HTTP-статус.
    :return: None.
    :raises AssertionError: Если фактический HTTP-статус ответа
    не совпадает с ожидаемым.
    """
    assert response.status_code == expected_status, \
        f'{response.request["REQUEST_METHOD"]}' \
        f' - {response.request["PATH_INFO"]}' \
        f' - {error_msg(response.status_code, expected_status)}'


def dict_to_namespace(data: Dict) -> SimpleNamespace:
    """
    Преобразует словарь в пространство имен (namespace)
    с помощью SimpleNamespace.
    :param data: Словарь, который нужно преобразовать.
    :return: Объект SimpleNamespace, содержащий данные из словаря.
    """
    return SimpleNamespace(**data)


def assert_200(response: Response) -> None:
    """
    Проверяет, что HTTP-статус ответа равен 200.
    :param response: Ответ от сервера.
    :return: None.
    """
    assert_method(response, status.HTTP_200_OK)


def assert_201(response: Response) -> None:
    """
    Проверяет, что HTTP-статус ответа равен 201.
    :param response: Ответ от сервера.
    :return: None.
    """
    assert_method(response, status.HTTP_201_CREATED)


def assert_205(response: Response) -> None:
    """
    Проверяет, что HTTP-статус ответа равен 205.
    :param response: Ответ от сервера.
    :return: None.
    """
    assert_method(response, status.HTTP_205_RESET_CONTENT)


def assert_400(response: Response) -> None:
    """
    Проверяет, что HTTP-статус ответа равен 400.
    :param response: Ответ от сервера.
    :return: None.
    """
    assert_method(response, status.HTTP_400_BAD_REQUEST)


def assert_401(response: Response) -> None:
    """
    Проверяет, что HTTP-статус ответа равен 401.
    :param response: Ответ от сервера.
    :return: None.
    """
    assert_method(response, status.HTTP_401_UNAUTHORIZED)


def session_init(client: Client) -> Tuple[SessionBase, CartData]:
    """
    Инициализирует сессию клиента и создает пустую корзину
    покупок в сессии.
    :param client: Объект клиента.
    :return: Кортеж (сессия, корзина).
    """
    session = client.session
    cart = session[settings.CART_SESSION_ID] = {}
    return session, cart


def adding_product_to_cart(cart: CartData, product: Product) -> CartData:
    """
    Добавляет продукт в корзину покупок в сессии клиента.
    :param cart: Корзина покупок.
    :param product: Продукт для добавления.
    :return: Обновленная корзина покупок.
    """
    cart.setdefault(str(product.id), {'count': 0, 'price': str(product.price)})
    cart[str(product.id)]['count'] += product.count
    return cart


def session_save(session: SessionBase, cart: CartData) -> None:
    """
    Сохраняет корзину покупок в сессии и помечает сессию как измененную.
    :param session: Сессия клиента.
    :param cart: Корзина покупок.
    :return: None.
    """
    session[settings.CART_SESSION_ID] = cart
    session.modified = True
    session.save()


def get_cart(client: Client) -> CartData:
    """
    Получает корзину покупок из сессии клиента.
    :param client: Объект клиента.
    :return: Корзина покупок.
    """
    session = client.session
    cart = session[settings.CART_SESSION_ID]
    return cart


def add_product_session(cart: CartData, product: Product, product_count: int):
    """
    Добавляет указанное количество продуктов в корзину покупок в сессии клиента.
    :param cart: Корзина покупок.
    :param product: Продукт для добавления.
    :param product_count: Количество продукта для добавления.
    :return: Обновленная корзина покупок.
    """
    cart.setdefault(str(product.id), {'count': 0, 'price': str(product.price)})
    cart[str(product.id)]['count'] += product_count


def create_product() -> Product:
    """
    Создает новый продукт, используя фабрики для создания:
    категории, продукта, изображения продукта и спецификаций продукта.
    :return: Экземпляр Product.
    """
    category = CategoriesFactory.create()
    product = ProductFactory.create(category=category)
    ProductImageFactory.create(product=product)
    ProductSpecificationsFactory.create(product=product)
    return product


def create_product_limited_edition() -> Product:
    """
    Создает новый продукт с ограниченным тиражом, используя фабрики для создания
    категории, продукта, изображения продукта и спецификаций продукта.
    :return: Экземпляр Product.
    """
    category = CategoriesFactory.create()
    product = ProductFactory.create(category=category, limited_edition=True)
    ProductImageFactory.create(product=product)
    ProductSpecificationsFactory.create(product=product)
    return product


def create_order(
    product: Product = None,
    user: User = None,
    status: str = None,
    delivery_type: str = None,
    payment_type: str = None
) -> Order:
    """
    Создает новый заказ с указанными параметрами.
    :param product: Экземпляр Product.
    :param user: Экземпляр User.
    :param status: Статус заказа.
    :param delivery_type: Тип доставки.
    :param payment_type: Тип оплаты.
    :return: Экземпляр Order.
    """
    if product is None:
        product = create_product()
    kwargs = {
        key: value for key, value in locals().items()
        if key != 'product' and value is not None
    }
    order = OrderFactory.create(**kwargs)
    OrderCountProductFactory.create(order=order, product=product)
    return order


def create_review(product: Product = None) -> Review:
    """
    Создает отзыв к продукту на основе переданного продукта
    или создает новый продукт, если он не был передан.
    :param product: Экземпляр Product.
    :return: Экземпляр Review.
    """
    if product is None:
        product = create_product()
    review = ReviewFactory.create(product=product)
    return review


def create_sale(product: Product = None) -> Sale:
    """
    Создает экземпляр Sale на основе переданного продукта
    или создает новый продукт, если он не был передан.
    :param product: Экземпляр Product.
    :return: Экземпляр Sale.
    """
    if product is None:
        product = create_product()
    sale = SaleFactory.create(product=product)
    return sale


def create_tag(product: Product = None) -> Tag:
    """
    Создает экземпляр Tag на основе переданного продукта
    или создает новый продукт, если он не был передан.
    :param product: Экземпляр Product.
    :return: Экземпляр Tag.
    """
    if product is None:
        product = create_product()
    tag = TagFactory.create()
    product.tags.add(tag)
    return tag


def create_payment_transaction(user: User) -> PaymentTransaction:
    """
    Создает платежную транзакцию для пользователя.
    :param user: Экземпляр User.
    :return: Экземпляр PaymentTransaction.
    """
    payment_transaction = PaymentTransactionFactory(user=user)
    return payment_transaction


def create_basket(user: User, product: Product = None) -> Basket:
    """
    Создает корзину для пользователя с определенным продуктом
    или случайным продуктом, если продукт не указан.
    :param user: Экземпляр User.
    :param product: Экземпляр Product.
    :return: Экземпляр Basket
    """
    if product is None:
        product = create_product()
    basket = BasketFactory.create(user=user, product=product)
    return basket
