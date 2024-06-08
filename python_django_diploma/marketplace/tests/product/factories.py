import random
from datetime import timedelta, datetime

import factory
from faker import Faker

from tests.catalog.factories import CategoriesFactory
from product.models import (
    Product, ProductImage, Tag,
    Review, ProductSpecifications, Sale
)


fake = Faker()


class TagFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Tag

    name = fake.text(max_nb_chars=50)


class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Product

    title = fake.text(max_nb_chars=100)
    description = fake.text(max_nb_chars=1000)
    full_description = fake.text(max_nb_chars=1000)
    category = factory.SubFactory(CategoriesFactory)
    tags = factory.RelatedFactoryList(TagFactory, size=2)
    free_delivery = fake.boolean()
    limited_edition = fake.boolean()
    date = fake.date()
    price = fake.random_int()
    count = fake.random_int()
    rating = fake.pydecimal(
        left_digits=1,
        right_digits=1,
        positive=True,
        min_value=1,
        max_value=10
    )


class ProductImageFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ProductImage

    product = factory.SubFactory(ProductFactory)
    src = factory.django.ImageField(filename='product/image.jpg')
    alt = fake.text(max_nb_chars=50)


class ReviewFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Review

    author = fake.text(max_nb_chars=50)
    email = fake.email()
    product = factory.SubFactory(ProductFactory)
    text = fake.text(max_nb_chars=1000)
    rate = random.randint(1, 10)


class ProductSpecificationsFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ProductSpecifications

    name = fake.text(max_nb_chars=150)
    value = fake.text(max_nb_chars=100)
    product = factory.SubFactory(ProductFactory)


class SaleFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Sale

    product = factory.SubFactory(ProductFactory)
    sale_price = fake.random_int()
    date_from = fake.date()
    date_to = factory.LazyAttribute(
        lambda obj: (
            datetime.strptime(obj.date_from, '%Y-%m-%d') +
            timedelta(days=29)).strftime('%Y-%m-%d')
    )
