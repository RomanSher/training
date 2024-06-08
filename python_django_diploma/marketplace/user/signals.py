from django.db.models.signals import pre_save
from django.dispatch import receiver

from project.exceptions import UserAvatarSizeError
from user.models import User


@receiver(pre_save, sender=User)
def validate_avatar_size(sender, instance, **kwargs) -> None:
    """
    Проверяет размер аватара пользователя перед сохранением.
    :param sender: Модель, отправляющая сигнал (User).
    :param instance: Экземпляр User.
    :param kwargs: Дополнительные аргументы.
    :return: None.
    """
    megabyte_limit = 2 * 1024 * 1024
    if instance.avatar and instance.avatar.size > megabyte_limit:
        raise UserAvatarSizeError
