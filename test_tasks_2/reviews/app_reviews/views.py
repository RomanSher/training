from .models import *
from .serializers import *
from rest_framework import generics
from django.http import HttpResponseBadRequest
from rest_framework.permissions import AllowAny
from .utils import *
from django.http import HttpResponse



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

