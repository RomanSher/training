from multiprocessing.connection import Client

import pytest
from django.urls import reverse

from tests.utils import assert_200, create_tag


@pytest.mark.django_db
def test_tag(client: Client) -> None:
    """
    Проверяет, что теги отображаются корректно.
    :param client: Объект, представляющий клиента, который
    используется для взаимодействия с веб-сервером.
    :return: None.
    """
    tag = create_tag()
    url = reverse('tags')
    response = client.get(url, content_type='application/json')
    assert_200(response)
    assert response.data[int(tag.id) - 1]['id'] == tag.id
    assert response.data[int(tag.id) - 1]['name'] == tag.name
