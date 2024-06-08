import factory
from faker import Faker

from catalog.models import Categories


fake = Faker()


class CategoriesFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Categories

    title = fake.text(max_nb_chars=100)
    src = factory.django.ImageField(filename='categories/image.jpg')
    alt = fake.text(max_nb_chars=50)
    favorites = fake.boolean()
    parent = None
