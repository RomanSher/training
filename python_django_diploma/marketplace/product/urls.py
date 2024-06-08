from django.urls import path
from product.views import (
    ProductDetailAPIView, ProductReviewAPIView, TagAPIView,
    ProductPopularAPIView, ProductLimitedAPIView, SaleAPIView,
    BannerAPIView
 )

urlpatterns = [
    path('product/<int:pk>/', ProductDetailAPIView.as_view(), name='product'),
    path('product/<int:pk>/reviews/', ProductReviewAPIView.as_view(), name='product-review'),
    path('tags/', TagAPIView.as_view(), name='tags'),
    path('sales/', SaleAPIView.as_view(), name='sales'),
    path('banners/', BannerAPIView.as_view(), name='banners'),
    path('products/popular/', ProductPopularAPIView.as_view(), name='product-popular'),
    path('products/limited/', ProductLimitedAPIView.as_view(), name='product-limited'),
]

