import factory
from faker import Faker

from basket.models import Basket
from tests.product.factories import ProductFactory
from tests.users.factories import UserFactory


fake = Faker()


class BasketFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Basket

    product = factory.SubFactory(ProductFactory)
    user = factory.SubFactory(UserFactory)
    count = fake.random_int()
    price = fake.random_int()
