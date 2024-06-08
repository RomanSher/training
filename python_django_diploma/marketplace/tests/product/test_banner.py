from multiprocessing.connection import Client

import pytest
from django.urls import reverse

from product.serializers import ProductSerializer
from tests.utils import assert_200, create_product, get_auth_client


@pytest.mark.django_db
def test_banner(client: Client) -> None:
    """
    Проверяет, что баннеры отображаются корректно.
    :param client: Объект, представляющий клиента, который
    используется для взаимодействия с веб-сервером.
    :return: None.
    """
    product = create_product()
    client, user = get_auth_client(client)
    url = reverse('banners')
    response = client.get(url, content_type='application/json')
    assert_200(response)
    expected_data = ProductSerializer([product], many=True).data
    for image in expected_data[0]['images']:
        image['src'] = 'http://testserver' + image['src']
    assert response.data == expected_data
