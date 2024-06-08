from django.urls import path
from catalog.views import CategoriesAPIView, CatalogViewSet, CatalogDetailViewSet


urlpatterns = [
    path('categories/', CategoriesAPIView.as_view(), name='categories'),
    path('catalog/', CatalogViewSet.as_view({'get': 'list'}), name='catalog'),
    path('catalog/<int:pk>/', CatalogDetailViewSet.as_view({'get': 'list'}), name='catalog-detail'),
]
