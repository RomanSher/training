from django.db import models
import datetime


class Сountry(models.Model):
    name = models.CharField(max_length=50, verbose_name='Название страны')

    def __str__(self):
        return self.name

class Manufacturer(models.Model):
    name = models.CharField(max_length=200, verbose_name='Название компании')
    country = models.ForeignKey(
        'Сountry', on_delete=models.CASCADE, related_name='country', verbose_name='Название страны'
    )

    def __str__(self):
        return self.name


class Car(models.Model):
    YEAR_CHOICES = [(y, y) for y in range(1900, datetime.date.today().year + 1)]

    name = models.CharField(max_length=200, verbose_name='Название машины')
    manufacturer = models.ForeignKey(
        'Manufacturer', on_delete=models.CASCADE,
        related_name='manufacturer',
        verbose_name='Название компании'
    )
    year_release = models.IntegerField(
        choices=YEAR_CHOICES,
        default=datetime.datetime.now().year,
        verbose_name='Год начала выпуска'
    )
    year_end = models.IntegerField(
        choices=YEAR_CHOICES,
        default=datetime.datetime.now().year,
        verbose_name='Год окончания выпуска'
    )

    def __str__(self):
        return self.name


class Comment(models.Model):
    email = models.EmailField()
    car = models.ForeignKey(
        'Car', on_delete=models.CASCADE, related_name='car', verbose_name='Название машины'
    )
    created_at = models.DateTimeField(format('%m/%d/%y %H:%M:%S'), auto_now_add=True)
    comment = models.CharField(max_length=1000, verbose_name='Комментарий')
