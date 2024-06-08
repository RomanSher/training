from multiprocessing.connection import Client

import pytest
from django.urls import reverse

from tests.utils import create_test_user


@pytest.mark.django_db
@pytest.mark.parametrize('username, password, expected_status', [
    ('ivanov', 'password123', 200),
    ('ivanov', 'password', 400),
    ('ivanov111', 'password123', 400)
])
def test_user_login(client: Client, username: str, password: str, expected_status: str) -> None:
    """
    Этот тест проверяет функционал входа пользователя.
    Он использует параметризацию для проведения нескольких тестов
    с разными данными входа пользователя. Тест проверяет, что при
    правильном вводе данных (правильное имя пользователя и пароль)
    ожидается успешный ответ от сервера с кодом 200, а при неправильных
    данных - код ответа 400 и соответствующее сообщение об ошибке.
    :param client: Объект, представляющий клиента, который
    используется для взаимодействия с веб-сервером.
    :param username: Имя пользователя для входа.
    :param password: Пароль пользователя.
    :param expected_status: Ожидаемый статус код ответа.
    :return: None.
    """
    create_test_user(username='ivanov', password='password123')
    url = reverse('sign-in')
    response = client.post(url, {
        'username': username,
        'password': password,
    })
    assert response.status_code == expected_status
    if expected_status == 200:
        assert 'access' in response.data
    else:
        assert 'non_field_errors' in response.data
