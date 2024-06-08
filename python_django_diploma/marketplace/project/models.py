from typing import Optional, Dict

from django.db import models
from django.db.models import QuerySet
from django.utils import timezone


class TimeStampedModel(models.Model):
    """
    Абстрактная модель с автоматическим добавлением временных меток создания
    и обновления записи.
    """
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        abstract = True


class SoftDeletionQuerySet(QuerySet):

    def delete(self) -> QuerySet:
        for instance in self:
            instance.delete()
        return self

    def hard_delete(self) -> Dict:
        return super(SoftDeletionQuerySet, self).delete()

    def alive(self) -> QuerySet:
        return self.filter(deleted_at=None)

    def dead(self) -> QuerySet:
        return self.exclude(deleted_at=None)


class SoftDeletionManager(models.Manager):

    def __init__(self, *args, **kwargs) -> None:
        self.alive_only = kwargs.pop('alive_only', True)
        super(SoftDeletionManager, self).__init__(*args, **kwargs)

    def get_queryset(self) -> 'QuerySet[SoftDeletionModel]':
        if self.alive_only:
            return SoftDeletionQuerySet(self.model).filter(deleted_at=None)
        return SoftDeletionQuerySet(self.model)

    def hard_delete(self) -> QuerySet:
        return self.get_queryset().hard_delete()


class SoftDeletionModel(TimeStampedModel):
    """ Абстрактная модель с поддержкой мягкого удаления записей из базы данных. """

    deleted_at = models.DateTimeField(null=True, blank=True, default=None)
    objects = SoftDeletionManager()
    all_objects = SoftDeletionManager(alive_only=False)

    def clean(self, delete: bool = False) -> None:
        pass

    def delete(self, using: Optional[str] = None, keep_parents: bool = False) -> None:
        self.clean(delete=True)
        self.deleted_at = timezone.now()
        self.save(using=using)

    def hard_delete(self) -> None:
        super(SoftDeletionModel, self).delete()

    class Meta:
        abstract = True
