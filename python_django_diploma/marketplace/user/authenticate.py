from django.contrib.auth.models import AnonymousUser
from django.views import View
from rest_framework.permissions import BasePermission
from rest_framework.request import Request


class AnonymousUserBackend:
    def get_user(self) -> AnonymousUser:
        """
        Возвращает анонимного пользователя.
        :return: Объект анонимного пользователя.
        """
        return AnonymousUser()


class IsNotAuthenticated(BasePermission):
    def has_permission(self, request: Request, view: View) -> bool:
        """
        Проверяет, аутентифицирован ли пользователь.
        :param request: Объект запроса.
        :param view: Представление.
        :return: True, если пользователь не аутентифицирован,
        иначе False.
        """
        return not request.user.is_authenticated
