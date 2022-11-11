from import_export import resources
from .models import *


class СountryResource(resources.ModelResource):
    class Meta:
        model = Сountry


class ManufacturerResource(resources.ModelResource):
    class Meta:
        model = Manufacturer


class СarResource(resources.ModelResource):
    class Meta:
        model = Car


class CommentResource(resources.ModelResource):
    class Meta:
        model = Comment



