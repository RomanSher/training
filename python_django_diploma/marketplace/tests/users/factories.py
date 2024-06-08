import factory
from faker import Faker

from user.models import User


fake = Faker()


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    fullName = fake.text(max_nb_chars=50)
    email = fake.email()
    phone = fake.random_int()
    avatar = fake.image()
