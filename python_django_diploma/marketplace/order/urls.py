from django.urls import path
from order.views import OrdersAPIView, OrdersDetailAPIView, PaymentTransactionsAPIView


urlpatterns = [
    path('orders/', OrdersAPIView.as_view(), name='orders'),
    path('orders/<int:pk>/', OrdersDetailAPIView.as_view(), name='orders-detail'),
    path('payment/<int:pk>/', PaymentTransactionsAPIView.as_view(), name='payment'),
]

