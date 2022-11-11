from rest_framework import serializers
from .models import *


class СountrySerializer(serializers.ModelSerializer):
    manufacturer = serializers.SerializerMethodField(method_name='get_manufacturer')

    class Meta:
        model = Сountry
        fields = ['id', 'name', 'manufacturer']


    def get_manufacturer(self, obj):
        queryset = Manufacturer.objects.filter(country__id=obj.id).values_list('name', flat=True)
        return queryset


class ManufacturerSerializer(serializers.ModelSerializer):
    car = serializers.SerializerMethodField(method_name='get_car')
    num_comments_cars = serializers.SerializerMethodField(method_name='get_number_of_comments_on_cars')
    country = serializers.StringRelatedField()

    class Meta:
        model = Manufacturer
        fields = ['id', 'name', 'country', 'car', 'num_comments_cars']


    def get_car(self, obj):
        queryset = Car.objects.filter(manufacturer__id=obj.id).values_list('name', flat=True)
        return queryset


    def get_number_of_comments_on_cars(self, obj):
        car = Car.objects.filter(manufacturer_id=obj.id).values_list('id', flat=True)
        queryset = Comment.objects.filter(car__id__in=car).count()
        return queryset


class CarSerializer(serializers.ModelSerializer):
    comment = serializers.SerializerMethodField(method_name='get_comment')
    num_comments = serializers.SerializerMethodField(method_name='get_numbers_of_comments')
    manufacturer = serializers.StringRelatedField()

    class Meta:
        model = Car
        fields = ['id', 'name', 'manufacturer', 'year_release', 'year_end', 'comment', 'num_comments']


    def get_comment(self, obj):
        queryset = Comment.objects.filter(car__id=obj.id).values_list('comment', flat=True)
        return queryset

    def get_numbers_of_comments(self, obj):
        queryset = Comment.objects.filter(car__id=obj.id).count()
        return queryset


class CommentSerializer(serializers.ModelSerializer):
    car = serializers.StringRelatedField()

    class Meta:
        model = Comment
        fields = ['id', 'email', 'car', 'created_at', 'comment']
