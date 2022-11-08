from rest_framework import serializers
from .models import *



class СountrySerializer(serializers.ModelSerializer):
    manufacturer = serializers.CharField(source='get_manufacturer', read_only=True)

    class Meta:
        model = Сountry
        fields = ['id', 'name', 'manufacturer']


class ManufacturerSerializer(serializers.ModelSerializer):
    car = serializers.CharField(source='get_car', read_only=True)
    num_comments_cars = serializers.IntegerField(source='number_of_comments_on_cars', read_only=True)

    class Meta:
        model = Manufacturer
        fields = ['id', 'name', 'country', 'car', 'num_comments_cars']

    def to_representation(self, instance):
        rep = super(ManufacturerSerializer, self).to_representation(instance)
        rep['country'] = instance.country.name
        return rep


class CarSerializer(serializers.ModelSerializer):
    comment = serializers.CharField(source='get_comment', read_only=True)
    num_comments = serializers.IntegerField(source='numbers_of_comments', read_only=True)

    class Meta:
        model = Car
        fields = ['id', 'name', 'manufacturer', 'year_release', 'year_end', 'comment', 'num_comments']


    def to_representation(self, instance):
        rep = super(CarSerializer, self).to_representation(instance)
        rep['manufacturer'] = instance.manufacturer.name
        return rep


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'email', 'car', 'created_at', 'comment']

    def to_representation(self, instance):
        rep = super(CommentSerializer, self).to_representation(instance)
        rep['car'] = instance.car.name
        return rep