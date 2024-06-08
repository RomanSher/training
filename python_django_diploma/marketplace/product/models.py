from typing import List

from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MaxValueValidator, MinValueValidator

from catalog.models import Categories
from project.models import TimeStampedModel


class Product(TimeStampedModel):
    """ Модель товара. """

    title = models.CharField(max_length=100, verbose_name=_('name'))
    description = models.TextField(max_length=1000, verbose_name=_('description'))
    full_description = models.TextField(
        max_length=1000,
        blank=True,
        verbose_name=_('full description')
    )
    price = models.IntegerField(default=0, verbose_name=_('product price'))
    count = models.IntegerField(default=0, verbose_name=_('quantity goods'))
    category = models.ForeignKey(
        Categories,
        on_delete=models.CASCADE,
        verbose_name=_('category product')
    )
    tags = models.ManyToManyField('Tag', blank=True, verbose_name=_('tags'))
    free_delivery = models.BooleanField(
        blank=True,
        default=False,
        verbose_name=_('free delivery')
    )
    limited_edition = models.BooleanField(default=False, verbose_name=_('limited edition'))
    date = models.DateTimeField(auto_now_add=True, verbose_name=_('creation time'))
    rating = models.FloatField(
        default=0,
        validators=[MinValueValidator(0.0), MaxValueValidator(10.0)],
        verbose_name=_('rating')
    )

    class Meta:
        verbose_name_plural = _('Products')
        verbose_name = _('Product')

    def __str__(self):
        return self.title

    @property
    def product_images(self) -> List[str]:
        """
        Получение изображений товара и их описание
        :return: ссылка на изоображение
        """
        return [f'/media/{image}' for image in self.images.all()]

    def href(self) -> str:
        """
        Получение ссылки на детальную страницу товара
        :return: ссылка
        """
        return f'/product/{self.id}'

    def reviews(self) -> int:
        """
        Получение количества отзывов на товар
        :return: количество отзывов
        """
        return self.review_set.count()

    def update_rate(self) -> None:
        """
        Пересчитывает и обновляет среднюю оценку товара
        на основе отзывов, которые о нем написаны.
        :return: None.
        """
        reviews = self.review_set.all()
        total_rating = sum([review.rate for review in reviews])
        self.rating = total_rating / len(reviews)
        self.save()


class ProductImage(TimeStampedModel):
    """ Модель изображение товара. """

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name=_('product')
    )
    src = models.ImageField(upload_to='product/', verbose_name=_('image'))
    alt = models.CharField(max_length=50, verbose_name=_('image description'))

    def __str__(self):
        return str(self.alt)

    class Meta:
        verbose_name_plural = _('Product images')
        verbose_name = _('Product image')


class Sale(TimeStampedModel):
    """ Модель товаров со скидкой. """

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name=_('product')
    )
    sale_price = models.IntegerField(default=0, verbose_name=_('sale price'))
    date_from = models.DateField(verbose_name=_('date from'))
    date_to = models.DateField(verbose_name=_('date to'))

    class Meta:
        verbose_name = _('Sale')
        verbose_name_plural = _('Sales')
        ordering = ['pk', ]

    def title(self) -> str:
        """
        Получение названия товара.
        :return: Название товара.
        """
        return self.product.title

    def price(self) -> int:
        """
        Получение Первоначальной цены товара.
        :return: Цена.
        """
        return self.product.price

    def href(self) -> str:
        """
        Получение Ссылки на детальную страницу товара.
        :return: Ссылка.
        """
        return f'/product/{self.product_id}'


class Tag(TimeStampedModel):
    """ Модель тегов для товара. """

    name = models.CharField(max_length=50, verbose_name=_('tag name'))

    class Meta:
        verbose_name_plural = _('Tags')
        verbose_name = _('Tag')


class Review(TimeStampedModel):
    """ Модель отзыва на товар. """

    author = models.CharField(max_length=50, verbose_name=_('author'))
    email = models.EmailField(verbose_name=_('email'))
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name=_('product')
    )
    text = models.TextField(max_length=1000, verbose_name=_('comment'))
    rate = models.PositiveSmallIntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(10)],
        verbose_name=_('rate')
    )

    class Meta:
        verbose_name_plural = _('Reviews')
        verbose_name = _('Review')

    def __str__(self):
        return self.author


class ProductSpecifications(TimeStampedModel):
    """ Модель характеристик товара. """

    name = models.CharField(max_length=150)
    value = models.CharField(max_length=100)
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name=_('product')
    )

    class Meta:
        verbose_name_plural = _('Product specifications')
        verbose_name = _('Product specification')

    def __str__(self):
        return self.name
