from django.db import models

class News(models.Model):
    title = models.CharField(max_length=200, verbose_name='Заголовок')
    description = models.CharField(max_length=2000, verbose_name='Текст статьи')
    created_at = models.DateTimeField(format('%m/%d/%y %H:%M:%S'), auto_now_add=True)
    picture = models.ImageField()

    def __str__(self):
        return self.title