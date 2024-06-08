from typing import Dict

from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class ProductPagination(PageNumberPagination):
    page_size = 10
    page_query_param = 'currentPage'

    def get_paginated_response(self, data: Dict) -> Response:
        """
        Возвращает ответ с данными, разбитыми на страницы.
        :param data: Данные, которые нужно разбить на страницы.
        :return: Ответ с данными, номером текущей страницы и
        номером последней страницы.
        """
        return Response(
            {
                'items': data,
                'currentPage': self.page.number,
                'lastPage': self.page.paginator.num_pages,
            }
        )
