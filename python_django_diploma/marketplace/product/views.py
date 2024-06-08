from django.db.models import Sum, Q
from rest_framework.generics import ListCreateAPIView, ListAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated

from order.models import Order
from product.models import Product, Review, Tag, Sale
from product.pagination import ProductPagination
from product.serializers import (
    ProductSerializer, ProductDetailSerializer, TagSerializer,
    SaleSerializer, ReviewSerializer
)


class BannerAPIView(ListAPIView):
    queryset = Product.objects.prefetch_related(
        'productimage_set',
        'tags',
        'review_set'
    )[:5]
    serializer_class = ProductSerializer
    permission_classes = (AllowAny,)


class ProductDetailAPIView(RetrieveAPIView):
    queryset = Product.objects.prefetch_related(
        'productimage_set',
        'review_set',
        'tags',
        'sale_set',
        'productspecifications_set'
    )
    serializer_class = ProductDetailSerializer
    permission_classes = (AllowAny,)
    lookup_field = 'pk'


class ProductReviewAPIView(ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = 'pk'


class ProductPopularAPIView(ListAPIView):
    queryset = Product.objects.annotate(
        total_count=Sum(
            'ordercountproduct__count',
            filter=Q(
                ordercountproduct__order__status__in=[
                    Order.PAID, Order.COMPLETED
                ]
            )
        )
    ).prefetch_related(
        'productimage_set',
        'tags',
        'review_set'
    ).order_by('-total_count')[:8]
    serializer_class = ProductSerializer
    permission_classes = (AllowAny,)


class ProductLimitedAPIView(ListAPIView):
    queryset = Product.objects.filter(
        limited_edition=True
    ).prefetch_related(
        'productimage_set',
        'tags',
        'review_set'
    )[:16]
    serializer_class = ProductSerializer
    permission_classes = (AllowAny,)


class SaleAPIView(ListAPIView):
    queryset = Sale.objects.select_related(
        'product'
    ).prefetch_related(
        'product__productimage_set'
    )
    serializer_class = SaleSerializer
    pagination_class = ProductPagination
    permission_classes = (AllowAny,)


class TagAPIView(ListAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (AllowAny,)
