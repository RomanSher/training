from multiprocessing.connection import Client

import pytest
from django.urls import reverse

from tests.utils import assert_200, create_sale, create_product


@pytest.mark.django_db
def test_sale(client: Client) -> None:
    """
    Проверяет, что продукты с распродажей отображаются корректно.
    :param client: Объект, представляющий клиента, который
    используется для взаимодействия с веб-сервером.
    :return: None.
    """
    product = create_product()
    sale = create_sale(product=product)
    url = reverse('sales')
    response = client.get(url, content_type='application/json')
    assert_200(response)
    assert response.data['items'][0]['sale_price'] == sale.sale_price
    assert response.data['items'][0]['date_from'] == sale.date_from
    assert response.data['items'][0]['date_to'] == sale.date_to
    assert response.data['items'][0]['product'] == sale.product.id
