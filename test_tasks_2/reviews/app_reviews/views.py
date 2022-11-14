from rest_framework.viewsets import GenericViewSet
from .models import *
from .serializers import *
from rest_framework import generics
from django.http import HttpResponseBadRequest
from rest_framework.permissions import AllowAny
from .utils import *


class ExportViewSet(DataMixin, GenericViewSet):

    def dispatch(self, request, *args, **kwargs):
        query = ''.join(request.GET)
        if query == 'country':
            model = Сountry
        elif query == 'manufacturer':
            model = Manufacturer
        elif query == 'car':
            model = Car
        elif query == 'comment':
            model = Comment
        else:
            return HttpResponseBadRequest

        format = self.request.GET.get(query)
        if format == 'xlsx':
            result = self.export_xlsx(model)
            return result
        elif format == 'csv':
            result = self.export_csv(model)
            return result
        else:
            return HttpResponseBadRequest


# Закомментированные строки - это решение с помощью библиотеки django import-export

# class ExportViewSet(DataMixin, GenericViewSet):
#
#     def dispatch(self, request, *args, **kwargs):
#         query = ''.join(request.GET)
#         if query == 'country':
#             model = Сountry
#             member_resource = СountryResource()
#         elif query == 'manufacturer':
#             model = Manufacturer
#             member_resource = ManufacturerResource()
#         elif query == 'car':
#             model = Car
#             member_resource = СarResource()
#         elif query == 'comment':
#             model = Comment
#             member_resource = CommentResource()
#         else:
#             return HttpResponseBadRequest
#
#         format = self.request.GET.get(query)
#         if format == 'xlsx':
#             result = self.export_xlsx(model, member_resource)
#             return result
#         elif format == 'csv':
#             result = self.export_csv(model, member_resource)
#             return result
#         else:
#             return HttpResponseBadRequest



class СountryAPICreateRead(generics.ListCreateAPIView):
    queryset = Сountry.objects.all()
    serializer_class = СountrySerializer


class ManufacturerAPICreateRead(generics.ListCreateAPIView):
    queryset = Manufacturer.objects.all()
    serializer_class = ManufacturerSerializer


class CarAPICreateRead(generics.ListCreateAPIView):
    queryset = Car.objects.all()
    serializer_class = CarSerializer


class CommentAPICreateRead(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (AllowAny,)


class СountryAPIUpdateDelete(generics.RetrieveUpdateDestroyAPIView):
    queryset = Сountry.objects.all()
    serializer_class = СountrySerializer


class ManufacturerAPIUpdateDelete(generics.RetrieveUpdateDestroyAPIView):
    queryset = Manufacturer.objects.all()
    serializer_class = ManufacturerSerializer


class CarAPIUpdateDelete(generics.RetrieveUpdateDestroyAPIView):
    queryset = Car.objects.all()
    serializer_class = CarSerializer


class CommentAPIUpdateDelete(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

