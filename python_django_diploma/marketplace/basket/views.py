from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet

from basket.serializers import BasketSerializer
from basket.cart import Cart


class BasketAPIView(ModelViewSet):
    serializer_class = BasketSerializer
    permission_classes = (AllowAny,)

    def get_queryset(self):
        return Cart(self.request).store_products_in_cart()

    def create(self, request, *args, **kwargs):
        Cart(self.request).add_product_or_update()
        return Response(status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        Cart(self.request).reduce_product_or_update()
        return Response(status=status.HTTP_200_OK)
