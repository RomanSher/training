from multiprocessing.connection import Client

import pytest
from django.urls import reverse

from tests.utils import (
    assert_200, dict_to_namespace, get_auth_client_full, assert_400
)


@pytest.mark.django_db
class TestProfileUser:

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
        self.client, self.user = get_auth_client_full(client)
        self.url_1 = reverse('profile')
        self.url_2 = reverse('profile-password')
        self.url_3 = reverse('profile-avatar')

    def test_get_user_profile(self) -> None:
        """
        Тест для получения профиля пользователя.
        Проверяет, что при запросе профиля пользователя возвращается
        ожидаемая информация.
        :return: None.
        """
        response = self.client.get(self.url_1)
        assert_200(response)
        data = dict_to_namespace(response.data)
        assert data.full_name == self.user.full_name
        assert data.email == self.user.email
        assert data.phone == self.user.phone
        assert data.avatar == f'http://testserver/media/{self.user.avatar}'

    def test_update_user_profile(self) -> None:
        """
        Обновление профиля пользователя.
        Проверяется обновление полей 'fullName', 'email' и 'phone'.
        :return: None.
        """
        data = {
            'full_name': 'Ivanov ivan',
            'email': 'ivanov@example.com',
            'phone': '+79994443322'
        }
        response = self.client.patch(self.url_1, data, content_type=self.content_type)
        assert_200(response)
        assert response.data['full_name'] == data['full_name']
        assert response.data['email'] == data['email']
        assert response.data['phone'] == data['phone']

    def test_update_password_user_profile_successfully(self) -> None:
        """
        Тест для проверки обновления пароля в профиле пользователя.
        При помощи данного теста проверяется возможность обновления
        пароля пользователя. В данном случае вводится текущий пароль
        пользователя, а затем устанавливается новый пароль.
        После обновления пароля в профиле пользователя, производится
        проверка соответствия нового пароля в базе данных.
        :return: None.
        """
        data = {
            'password_current': '12wqasxz',
            'password': '12wqasxz1',
            'password_reply': '12wqasxz1'
        }
        self.user.set_password(data['password_current'])
        self.user.save()
        response = self.client.patch(self.url_2, data, content_type=self.content_type)
        assert_200(response)
        self.user.refresh_from_db()
        assert self.user.check_password(data['password'])

    def test_update_password_user_profile_not_successfully(self) -> None:
        """
        Тестирование не успешного обновления пароля пользовательского профиля.
        Тест проверяет сценарий, при котором пользователь указал два разных
        пароля для смены текущего пароля.
        """
        data = {
            'password_current': '12wqasxz',
            'password': '12wqasxz1',
            'password_reply': '12wqasxz12'
        }
        self.user.set_password(data['password_current'])
        self.user.save()
        response = self.client.patch(self.url_2, data, content_type=self.content_type)
        assert_400(response)
