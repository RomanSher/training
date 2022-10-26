import literals

from literals import LSTEP
from datetime import date
from .calendar_2 import second_date
from telebot.types import Message, CallbackQuery
from create_bot import bot, logger, exception_handler
from telegram_bot_calendar import DetailedTelegramCalendar


def first_date(message: Message) -> None:

    """
    Функция запрашивающая у пользователя дату заезда в отель.
    После запроса для взаимодействия с пользователем создаёт inline-календарь.
    :param message: Message
    :return: None
    """

    logger.info(str(message.from_user.id))
    calendar, step = DetailedTelegramCalendar(calendar_id=1).build()
    bot.send_message(message.chat.id, f'{literals.CHOOSE} {LSTEP[step]}', reply_markup=calendar)


@bot.callback_query_handler(func=DetailedTelegramCalendar.func(calendar_id=1))
def cal(call: CallbackQuery) -> None:

    """
    Функция - обработчик inline-календаря. Реагирует только на календарь с id = 1.
    После обработки пользовательской информации, перенаправляет в функцию
    calendar.second_date.
    :param call: CallbackQuery
    :return: None
    """

    logger.info(str(call.from_user.id))
    result, key, step = DetailedTelegramCalendar(
    min_date=date.today(), calendar_id=1, locale='ru').process(call.data)

    if not result and key:
        bot.edit_message_text(f'{literals.CHOOSE} {LSTEP[step]}',
        call.message.chat.id, call.message.message_id, reply_markup=key)

    elif result:
        bot.edit_message_text(f'{literals.SELECTED} {result}',
        call.message.chat.id, call.message.message_id)
        with bot.retrieve_data(call.from_user.id, call.message.chat.id) as data:
            data['date_arrival'] = result
        second_date(call)





