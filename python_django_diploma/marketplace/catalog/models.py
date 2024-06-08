from django.db import models
from django.utils.translation import gettext_lazy as _
from mptt.models import MPTTModel, TreeForeignKey


class Categories(MPTTModel):
    """ Модель категорий товаров. """

    STATUS_CHOICES = [
        ('False', 'False'),
        ('True', 'True')
    ]
    title = models.CharField(max_length=100, verbose_name=_('category name'))
    parent = TreeForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='subcategories_set'
    )
    src = models.FileField(upload_to='categories/', verbose_name=_('image'))
    alt = models.CharField(max_length=50, verbose_name=_('image description'))
    favorites = models.CharField(
        max_length=5,
        choices=STATUS_CHOICES,
        blank=True,
        default='False',
        verbose_name=_('favorites')
    )

    class MPTTMeta:
        order_insertion_by = 'title'

    class Meta:
        verbose_name = _('category')
        verbose_name_plural = _('categories')

    def __str__(self):
        return self.title
