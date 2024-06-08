from multiprocessing.connection import Client

import pytest
from django.urls import reverse

from tests.utils import get_auth_client, assert_401, assert_205


@pytest.mark.django_db
def test_user_logout(client: Client) -> None:
    """
    Тест проверяет функционал выхода пользователя из системы.
    :param client: Объект, представляющий клиента, который
    используется для взаимодействия с веб-сервером.
    :return: None.
    """
    client, user = get_auth_client(client)
    url = reverse('sign-out')
    response = client.post(url)
    assert_205(response)


@pytest.mark.django_db
def test_no_auth(client: Client) -> None:
    """
    Тест проверяет функционал выхода пользователя из системы
    без предварительной аутентификации.
    :param client: Объект, представляющий клиента, который
    используется для взаимодействия с веб-сервером.
    :return: None.
    """
    url = reverse('sign-out')
    response = client.post(url)
    assert_401(response)
