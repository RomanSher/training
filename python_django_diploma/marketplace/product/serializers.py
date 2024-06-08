from django.db import transaction
from rest_framework import serializers

from product.models import (
    Tag, Review, ProductSpecifications,
    ProductImage, Product, Sale
)


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']


class ReviewSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format='%d-%m-%Y %H:%M:%S', required=False)

    class Meta:
        model = Review
        fields = ['author', 'email', 'text', 'rate', 'created_at']

    @transaction.atomic
    def create(self, validated_data):
        product_id =  self.context['request'].parser_context['kwargs'].get('pk')
        validated_data['product_id'] = product_id
        review = Review.objects.create(**validated_data)
        Product.objects.get(id=product_id).update_rate()
        return review


class ProductSpecificationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductSpecifications
        fields = ['name', 'value']


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['src', 'alt']


class SaleSerializer(serializers.ModelSerializer):
    title = serializers.StringRelatedField()
    href = serializers.StringRelatedField()
    price = serializers.StringRelatedField()
    images = ProductImageSerializer(
        source='product.productimage_set',
        read_only=True,
        many=True
    )

    class Meta:
        model = Sale
        fields = '__all__'


class ProductDetailSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(source='productimage_set', read_only=True, many=True)
    reviews = ReviewSerializer(source='review_set', read_only=True, many=True)
    tags = TagSerializer(many=True, required=False)
    specifications = ProductSpecificationsSerializer(
        source='productspecifications_set',
        read_only=True,
        many=True
    )
    price = serializers.SerializerMethodField()
    href = serializers.StringRelatedField()

    class Meta:
        model = Product
        fields = '__all__'

    def get_price(self, instance):
        product = instance.sale_set.first()
        if product:
            instance.price = product.sale_price
            instance.save()
            return product.sale_price
        return instance.price


class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(source='productimage_set', read_only=True, many=True)
    tags = TagSerializer(many=True, required=False)
    reviews = serializers.StringRelatedField()
    href = serializers.StringRelatedField()

    class Meta:
        model = Product
        fields = [
            'id', 'category', 'price', 'count', 'date', 'title', 'description',
            'href', 'free_delivery', 'images', 'tags', 'reviews', 'rating'
        ]
