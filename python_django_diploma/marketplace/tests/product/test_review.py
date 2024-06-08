from multiprocessing.connection import Client

import pytest
from django.urls import reverse

from tests.product.factories import ReviewFactory
from tests.utils import (
    get_auth_client, create_review, create_product,
    assert_201, assert_200
)


@pytest.mark.django_db
def test_product_review(client: Client) -> None:
    """
    Проверяет, что отзывы о продукте отображаются корректно.
    :param client: Объект, представляющий клиента, который
    используется для взаимодействия с веб-сервером.
    :return: None.
    """
    client, user = get_auth_client(client)
    product = create_product()
    review = create_review()
    url = reverse('product-review', kwargs={'pk': product.id})
    response = client.get(url, content_type='application/json')
    assert_200(response)
    assert response.data[0]['author'] == review.author
    assert response.data[0]['email'] == review.email
    assert response.data[0]['text'] == review.text
    assert response.data[0]['rate'] == review.rate


@pytest.mark.django_db
def test_product_create_review(client: Client) -> None:
    """
    Проверяет, что отзывы о продукте создаются корректно.
    :param client: Объект, представляющий клиента, который
    используется для взаимодействия с веб-сервером.
    :return: None.
    """
    client, user = get_auth_client(client)
    product = create_product()
    create_review()
    url = reverse('product-review', kwargs={'pk': product.id})
    data = {
        'author': 'Иванов Иван',
        'email': 'ivanov@mail.ru',
        'text': 'Отличный товар',
        'rate': 5
    }
    assert ReviewFactory._meta.model.objects.count() == 1
    response = client.post(url, data, content_type='application/json')
    assert_201(response)
    assert ReviewFactory._meta.model.objects.count() == 2
