from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet

from catalog.models import Categories
from catalog.utils import product_sorting
from product.models import Product
from catalog.serializers import CategoriesSerializer
from product.serializers import ProductSerializer
from catalog.filters import CatalogRequestFilter
from catalog.pagination import CatalogPagination


class CategoriesAPIView(ListAPIView):
    queryset = Categories.objects.filter(level=0)
    serializer_class = CategoriesSerializer


class CatalogViewSet(ModelViewSet):
    queryset = Product.objects.prefetch_related(
        'productimage_set',
        'tags',
        'review_set'
    )
    serializer_class = ProductSerializer
    permission_classes = (AllowAny,)
    filter_backends = [DjangoFilterBackend]
    filterset_class = CatalogRequestFilter
    pagination_class = CatalogPagination

    def list(self, request, *args, **kwargs):
        sort_field = request.query_params.get('sort', 'id')
        sort_type = request.query_params.get('sort_type', 'dec')
        page_size = request.query_params.get('limit', self.pagination_class.page_size)
        current_page = request.query_params.get('current_page', self.pagination_class.current_page)

        self.pagination_class.page_size = int(page_size)
        self.pagination_class.page_number = int(current_page)

        queryset = self.filter_queryset(self.get_queryset())
        queryset = product_sorting(queryset, sort_field, sort_type)
        queryset = self.paginate_queryset(queryset)

        serializer = self.get_serializer(queryset, many=True)
        return self.get_paginated_response(serializer.data)


class CatalogDetailViewSet(CatalogViewSet):

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(
            Q(category_id=int(self.kwargs['pk']), category__level=1) |
            Q(category__tree_id=int(self.kwargs['pk']))
        )
