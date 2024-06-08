from multiprocessing.connection import Client

import pytest
from django.urls import reverse

from user.models import User
from tests.utils import assert_400, assert_201


@pytest.mark.django_db
class TestUserRegistration:

    @pytest.fixture(autouse=True)
    def setup(self, client: Client) -> None:
        """
        Фикстура setup устанавливает начальные данные для тестов.
        :param client: Объект, представляющий клиента, который
        используется для взаимодействия с веб-сервером.
        :return: None.
        """
        self.client = client
        self.content_type = 'application/json'
        self.url = reverse('sign-up')

    def test_successful_registration(self) -> None:
        """
        Проверка успешной регистрации пользователя. Отправляем запрос с данными для
        регистрации пользователя и проверяем, что данные были сохранены корректно.
        :return: None.
        """
        data = {
            'full_name': 'Иванов Иван Иванович',
            'username': 'ivanov',
            'email': 'ivanov@gmail.com',
            'password': 'password123',
            'password2': 'password123'
        }
        response = self.client.post(self.url, data, content_type=self.content_type)
        assert_201(response)
        assert response.data['full_name'] == data['full_name']
        assert response.data['username'] == data['username']
        assert response.data['email'] == data['email']
        assert response.data['password'] == data['password']
        assert response.data['password2'] == data['password2']

    def test_incorrect_password_registration(self) -> None:
        """
        Тест проверяет регистрацию пользователя с неправильным повторным вводом пароля.
        В данном случае, пароль 'password123' не соответствует повторному вводу 'password456'.
        Тест должен возвращать ошибку 400 Bad Request и убеждаться,
        что в ответе есть 'non_field_errors'.
        :return: None.
        """
        data = {
            'full_name': 'Петров Петр Петрович',
            'username': 'petrov12',
            'email': 'petrov12@mail.com',
            'password': 'password123',
            'password2': 'password456'
        }
        response = self.client.post(self.url, data, content_type=self.content_type)
        assert_400(response)
        assert 'non_field_errors' in response.data

    def test_existing_user(self) -> None:
        """
        Тест проверяет поведение системы при попытке создания пользователя
        с уже существующим именем пользователя и адресом электронной почты.
        :return: None.
        """
        data = {
            'full_name': 'Ronaldo Cristiano',
            'username': 'r7',
            'email': 'r7@gmail.com',
            'password': 'password123'
        }
        User.objects.create(**data)
        response = self.client.post(self.url, data, content_type=self.content_type)
        assert_400(response)
        assert 'username' and 'email' in response.data
