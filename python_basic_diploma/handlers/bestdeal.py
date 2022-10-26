import literals

from userstates import UserState
from telebot.types import Message
from keyboards.calendar import first_date
from range_exception import check_price, check_range
from create_bot import bot, logger, message_exception_handler


@bot.message_handler(state=UserState.minPrice, is_digit=True)
@message_exception_handler
def min_price(message: Message) -> None:

    """
    Функция, реагирует только на положительные целые числа.
    Если ответ корректный, запрашивает данные о максимальной цене,
    если нет, повторяет предыдущий запрос.
    :param message: Message
    :return: None
    """

    logger.info(str(message.from_user.id))
    bot.send_message(message.from_user.id, text=literals.MAX_PRICE)
    bot.set_state(message.from_user.id, UserState.maxPrice, message.chat.id)
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['min_hotel_price'] = message.text


@bot.message_handler(state=UserState.maxPrice, is_digit=True)
@message_exception_handler
def max_price(message: Message) -> None:

    """
    Функция, реагирует только на положительные целые числа.
    Если ответ корректный, то передает диапазон цен в функцию 'check_price'.
    Если максимальная цена выше минимальной, то запрашивается минимальное
    расстояние. В противном случае повторяет запрос о максимальной цене.
    :param message: Message
    :return: None
    """

    logger.info(str(message.from_user.id))
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['max_hotel_price'] = message.text
    result = check_price(
        message, data['min_hotel_price'], data['max_hotel_price']
    )
    if result:
        bot.send_message(message.chat.id, text=literals.MINIMUM_DISTANCE)
        bot.set_state(message.from_user.id, UserState.minDist, message.chat.id)



@bot.message_handler(state=UserState.minDist, is_digit=True)
@message_exception_handler
def min_distance(message: Message) -> None:

    """
    Функция, реагирует только на положительные целые числа.
    Если ответ корректный, запрашивает данные о максимальном расстоянии,
    если нет, повторяет запрос.
    :param message: Message
    :return: None
    """

    logger.info(str(message.from_user.id))
    bot.send_message(message.from_user.id, text=literals.MAXIMUM_DISTANCE)
    bot.set_state(message.from_user.id, UserState.maxDist, message.chat.id)
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['min_dist_center'] = message.text



@bot.message_handler(state=UserState.maxDist, is_digit=True)
@message_exception_handler
def max_distance(message: Message) -> None:

    """
    Функция, реагирует только на положительные целые числа.
    Если ответ корректный, то передает диапазон расстояния в функцию
    'check_range'. Если максимальное расстояние выше минимального,
    то осуществляется переход к файлу 'calendar.py' и функции 'fisrt_date'
    В противном случае повторяет запрос о максимальном расстоянии.
    :param message: Message
    :return: None
    """

    logger.info(str(message.from_user.id))
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['max_dist_center'] = message.text
    result = check_range(
        message, data['min_dist_center'], data['max_dist_center']
    )
    if result:
        bot.send_message(message.from_user.id, text=literals.CHECK_IN)
        first_date(message)

