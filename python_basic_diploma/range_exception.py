import math
import literals

from telebot.types import Message, CallbackQuery
from create_bot import bot, logger, exception_handler


@exception_handler
def check_price(message: Message, min_price: int, max_price: int) -> bool:

    """
    Функция сравнивает минимальный и максимальный прайс.
    В случае, если минимальный прайс больше или равен максимальному, то выводится
    сообщение и запрос будет повторен.
    :param message: Message
    :param min_price: int
    :param max_price: int
    :return: bool
    """

    logger.info(str(message.from_user.id))
    if int(min_price) < int(max_price):
        return True
    else:
        bot.send_message(message.from_user.id, text=literals.ERROR_PRICE)
        return False


@exception_handler
def check_range(message: Message, min_dist: int, max_dist: int) -> bool:
    """
    Функция сравнивает минимальное и максимальное расстояние.
    В случае, если минимальное больше или равно максимальному, то выводится
    сообщение и запрос будет повторен.
    :param message: Message
    :param min_dist: int
    :param max_dist: int
    :return: bool
    """

    logger.info(str(message.from_user.id))
    if int(min_dist) < int(max_dist):
        return True
    else:
        bot.send_message(message.from_user.id, text=literals.ERROR_DISTANCE)
        return False


@exception_handler
def rounding_distance(num: int, hotel_json: dict) -> int:

    """
    Функция находит расстояние отеля от центра города и преобразует её в int
    и округляет в большую сторону для дальнейшего сравнения.
    :param num: int
    :param city_json: dict
    :return: int
    """

    landmarks = hotel_json[num]['landmarks'][0]['distance']
    dist_split = landmarks.split()
    dist = dist_split[0].replace(',', '.')
    distance = math.ceil(float(dist))
    return distance


@exception_handler
def number_of_days(call: CallbackQuery, current: str) -> str:

    """
    Функция вычисляет полную стоимость проживания.
    :param call: CallbackQuery
    :param current: str
    :return: str
    """

    logger.info(str(call.from_user.id))
    with bot.retrieve_data(call.from_user.id, call.message.chat.id) as data:
        price_day = current.split()
        price = price_day[0].replace(',', '.')
        number_day = (data['date_departure'] - data['date_arrival']).days
        full_price = '%.3f' % round(number_day * float(price), 3)
        full = full_price.replace('.', ',')
        return str(full) + ' RUB'










