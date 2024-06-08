import random
from datetime import datetime
from typing import Dict

from constants import LIST_OF_ERRORS


def check_date(month: str, year: str) -> bool:
    """
    Проверяет, истек ли срок указанной даты относительно текущей даты.
    :param month: Месяц окончания действия карты.
    :param year: Год окончания действия карты.
    :return: Возвращает True, если указанная дата уже истекла, и False в противном случае.
    """
    year, month = int(year), int(month)
    current_date = datetime.now()
    expiration_date = datetime(year + 2000, month, 1)

    if expiration_date >= current_date:
        return False
    else:
        return True


def check_length(data: Dict) -> str or None:
    """
    Проверяет длину значений по указанным требованиям.
    :param data: Словарь, содержащий аргументы, длину которых необходимо проверить.
    :return: Сообщение об ошибке, если какой-либо аргумент не соответствует
    указанным требованиям к длине, или None, если все аргументы соответствуют
    требованиям к длине.
    """
    length_constraints = {
        'number': (16, 16),
        'month': (2, 2),
        'year': (2, 2),
        'code': (3, 3),
        'name': (2, 30)
    }
    for name, (min_length, max_length) in length_constraints.items():
        if not min_length <= len(data[name]) <= max_length:
            return f'Invalid length for argument "{name}"'

    return None


def random_error() -> str:
    """
    Эта функция возвращает случайно выбранное сообщение
    об ошибке из заранее определенного списка ошибок.
    :return: Сообщение об ошибке.
    """
    return random.choice(LIST_OF_ERRORS)

