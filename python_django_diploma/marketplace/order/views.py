from django.db import transaction
from rest_framework import status
from rest_framework.generics import RetrieveUpdateAPIView, ListAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView

from order.utils import ProcessingOrderCreation
from order.models import Order, PaymentTransaction
from order.tasks import process_payment
from order.serializers import (
    OrderSerializer, OrderUpdateSerializer, PaymentTransactionSerializer
)
from rest_framework.response import Response


class OrdersAPIView(ListAPIView):
    queryset = Order.objects.prefetch_related('products').all()
    serializer_class = OrderSerializer
    permission_classes = (AllowAny,)

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    @transaction.atomic
    def post(self, request):
        order = ProcessingOrderCreation(
            request.data,
            request.user,
            request.session
        ).creating_an_order()
        return Response(data={'id': order.pk})


class OrdersDetailAPIView(RetrieveUpdateAPIView):
    queryset = Order.objects.prefetch_related('products').all()
    serializer_class = OrderUpdateSerializer
    permission_classes = (AllowAny,)


class PaymentTransactionsAPIView(APIView):
    queryset = PaymentTransaction.objects.all()
    serializer_class = PaymentTransactionSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request, pk):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.validated_data['user_id'] = request.user.id
        serializer.validated_data['order_id'] = pk
        process_payment.delay(serializer.validated_data)
        return Response(status=status.HTTP_201_CREATED)
