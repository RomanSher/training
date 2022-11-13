from rest_framework.viewsets import GenericViewSet
from .models import *
from .serializers import *
from rest_framework import generics
from django.http import HttpResponseBadRequest
from rest_framework.permissions import AllowAny
from .utils import *

# Закомментированные строки решение с помощью библиотеки openpyxl


def export_country(request):
    member_resource = СountryResource()
    dataset = member_resource.export()
    format = request.GET['format']
    if format == 'xlsx':
        response = HttpResponse(dataset.xlsx, content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename="country.xlsx"'
        return response
    elif format == 'csv':
        response = HttpResponse(dataset.csv, content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="country.csv"'
        return response
    else:
        return HttpResponseBadRequest


def export_manufacturer(request):
    member_resource = ManufacturerResource()
    dataset = member_resource.export()
    format = request.GET['format']
    if format == 'xlsx':
        response = HttpResponse(dataset.xlsx, content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename="manufacturer.xlsx"'
        return response
    elif format == 'csv':
        response = HttpResponse(dataset.csv, content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="manufacturer.csv"'
        return response
    else:
        return HttpResponseBadRequest


def export_car(request):
    member_resource = СarResource()
    dataset = member_resource.export()
    format = request.GET['format']
    if format == 'xlsx':
        response = HttpResponse(dataset.xlsx, content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename="car.xlsx"'
        return response
    elif format == 'csv':
        response = HttpResponse(dataset.csv, content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="car.csv"'
        return response
    else:
        return HttpResponseBadRequest


def export_comment(request):
    member_resource = CommentResource()
    dataset = member_resource.export()
    format = request.GET['format']
    if format == 'xlsx':
        response = HttpResponse(dataset.xlsx, content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename="comment.xlsx"'
        return response
    elif format == 'csv':
        response = HttpResponse(dataset.csv, content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="comment.csv"'
        return response
    else:
        return HttpResponseBadRequest




# class ExportCountry(DataMixin, GenericViewSet):
#
#     def dispatch(self, request, *args, **kwargs):
#         format = self.request.GET.get('format')
#         model = Сountry
#         title = model.__name__.lower()
#         print(title)
#         if format == 'xlsx':
#             result = self.export_xlsx(model)
#             return result
#         elif format == 'csv':
#             result = self.export_csv(model)
#             return result
#         else:
#             return HttpResponseBadRequest
#
#
#
# class ExportManufacturer(DataMixin, GenericViewSet):
#
#     def dispatch(self, request, *args, **kwargs):
#         format = self.request.GET.get('format')
#         model = Manufacturer
#         if format == 'xlsx':
#             result = self.export_xlsx(model)
#             return result
#         elif format == 'csv':
#             result = self.export_csv(model)
#             return result
#         else:
#             return HttpResponseBadRequest
#
#
#
# class ExportCar(DataMixin, GenericViewSet):
#
#     def dispatch(self, request, *args, **kwargs):
#         format = self.request.GET.get('format')
#         model = Car
#         if format == 'xlsx':
#             result = self.export_xlsx(model)
#             return result
#         elif format == 'csv':
#             result = self.export_csv(model)
#             return result
#         else:
#             return HttpResponseBadRequest
#
#
#
# class ExportComment(DataMixin, GenericViewSet):
#
#     def dispatch(self, request, *args, **kwargs):
#         format = self.request.GET.get('format')
#         model = Comment
#         if format == 'xlsx':
#             result = self.export_xlsx(model)
#             return result
#         elif format == 'csv':
#             result = self.export_csv(model)
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

