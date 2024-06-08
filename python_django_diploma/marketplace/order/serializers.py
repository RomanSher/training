from rest_framework import serializers
from rest_framework.serializers import raise_errors_on_nested_writes

from order.models import Order, OrderCountProduct, PaymentTransaction
from product.serializers import ProductSerializer
from project.exceptions import OrderUpdateError


class OrderSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True)

    class Meta:
        model = Order
        fields = [
            'id', 'created_at', 'full_name', 'email', 'phone', 'delivery_type',
            'payment_type', 'total_cost', 'status', 'city', 'address', 'products'
        ]


class ProductUpdateSerializer(ProductSerializer):
    count = serializers.SerializerMethodField()
    price = serializers.SerializerMethodField()

    def get_count(self, instance):
        order_id = self.context['order_id']
        try:
            query = OrderCountProduct.objects.get(order_id=order_id, product=instance)
            return query.count
        except OrderCountProduct.DoesNotExist:
            return 0

    def get_price(self, instance):
        order_id = self.context['order_id']
        try:
            query = OrderCountProduct.objects.get(order_id=order_id, product=instance)
            return query.price
        except OrderCountProduct.DoesNotExist:
            return 0


class OrderUpdateSerializer(serializers.ModelSerializer):
    products = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = [
            'id', 'created_at', 'full_name', 'email', 'phone', 'delivery_type',
            'payment_type', 'total_cost', 'status', 'city', 'address', 'products'
        ]

    def get_products(self, instance):
        serializer = ProductUpdateSerializer(
            instance.products,
            many=True,
            context={'order_id': instance.id}
        )
        return serializer.data

    def update(self, instance, validated_data):
        raise_errors_on_nested_writes('update', self, validated_data)
        user = self.context['request'].user
        validated_data['user'] = user
        validated_data['status'] = Order.AWAITS_PAYMENT

        for attr, value in validated_data.items():
            if not value:
                raise OrderUpdateError(detail=attr)
            setattr(instance, attr, value)

        instance.save()
        return instance


class PaymentTransactionSerializer(serializers.ModelSerializer):
    number = serializers.CharField(max_length=16, required=True)
    name = serializers.CharField(max_length=100, required=True)
    month = serializers.CharField(max_length=2, required=True)
    year = serializers.CharField(max_length=4, required=True)
    code = serializers.CharField(max_length=3, required=True)

    class Meta:
        model = PaymentTransaction
        fields = '__all__'
        extra_kwargs = {
            'user': {'required': False},
            'order': {'required': False}
        }
