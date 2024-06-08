from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class CatalogPagination(PageNumberPagination):
    page_size = 20
    current_page = 1
    page_query_param = 'current_page'
    min_price = 0
    max_price = 500000

    def get_paginated_response(self, data):

        return Response({
            'current_page': self.page_number,
            'last_page': self.page.paginator.num_pages,
            'items': data
        })
