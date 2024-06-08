from django.urls import path
from basket.views import BasketAPIView


urlpatterns = [
    path('basket/', BasketAPIView.as_view({'get': 'list', 'post': 'create', 'delete': 'destroy'}), name='basket'),
]
