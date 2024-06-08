from rest_framework import serializers
from catalog.models import Categories


class SubCategoriesSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField(method_name='get_image')
    href = serializers.SerializerMethodField(method_name='get_link')

    class Meta:
        model = Categories
        fields = ['id', 'title', 'image', 'href']

    def get_image(self, instance):
        image = {
            'src': f'/media/{instance.src}',
            'alt': instance.alt
        }
        return image

    def get_link(self, instance):
        return f'/catalog/{instance.id}'


class CategoriesSerializer(serializers.ModelSerializer):
    subcategories = SubCategoriesSerializer(source='subcategories_set', read_only=True, many=True)
    image = serializers.SerializerMethodField(method_name='get_image')
    href = serializers.SerializerMethodField(method_name='get_link')

    class Meta:
        model = Categories
        fields = ['id', 'title', 'image', 'href', 'subcategories']

    def get_image(self, instance):
        image = {
            'src': f'/media/{instance.src}',
            'alt': instance.alt
        }
        return image

    def get_link(self, instance):
        return f'/catalog/{instance.id}'
