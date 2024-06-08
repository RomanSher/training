from rest_framework import serializers
from basket.cart import Cart
from product.serializers import ProductSerializer


class BasketSerializer(ProductSerializer):
    count = serializers.SerializerMethodField()
    price = serializers.SerializerMethodField()

    def get_count(self, instance):
        return Cart(self.context['request']).count_product_in_basket(str(instance.id))

    def get_price(self, instance):
        return Cart(self.context['request']).price_product_in_basket(str(instance.id))
