import factory
from faker import Faker

from order.models import Order, OrderCountProduct, PaymentTransaction
from tests.product.factories import ProductFactory
from tests.users.factories import UserFactory


fake = Faker()


class OrderFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Order

    full_name = fake.text(max_nb_chars=50)
    email = fake.email()
    phone = fake.phone_number()
    delivery_type = Order.DELIVERY_METHOD[0][0]
    payment_type = Order.PAYMENT_METHOD[0][0]
    status = Order.COMPLETED
    total_cost = fake.random_int()
    city = fake.text(max_nb_chars=50)
    address = fake.text()


class OrderCountProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = OrderCountProduct

    order = factory.SubFactory(OrderFactory)
    product = factory.SubFactory(ProductFactory)
    count = fake.random_int()
    price = fake.random_int()


class PaymentTransactionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = PaymentTransaction

    order = factory.SubFactory(OrderFactory)
    user = factory.SubFactory(UserFactory)
    status = PaymentTransaction.STATUS_CHOICES[0][0]
