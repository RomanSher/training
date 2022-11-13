"""reviews URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from app_reviews.views import *
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

# Закомментированные строки решение с помощью библиотеки openpyxl

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/country/', СountryAPICreateRead.as_view()),
    path('api/manufacturer/', ManufacturerAPICreateRead.as_view()),
    path('api/car/', CarAPICreateRead.as_view()),
    path('api/comment/', CommentAPICreateRead.as_view()),
    path('api/country/<int:pk>/', СountryAPIUpdateDelete.as_view()),
    path('api/manufacturer/<int:pk>/', ManufacturerAPIUpdateDelete.as_view()),
    path('api/car/<int:pk>/', CarAPIUpdateDelete.as_view()),
    path('api/comment/<int:pk>/', CommentAPIUpdateDelete.as_view()),
    # path('api/export/country/', ExportCountry.as_view({'get': 'dispatch'})),
    # path('api/export/manufacturer/', ExportManufacturer.as_view({'get': 'dispatch'})),
    # path('api/export/car/', ExportCar.as_view({'get': 'dispatch'})),
    # path('api/export/comment/', ExportComment.as_view({'get': 'dispatch'})),
    path('api/export/country/', export_country),
    path('api/export/manufacturer/', export_manufacturer),
    path('api/export/car/', export_car),
    path('api/export/comment/', export_comment),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify')
]
