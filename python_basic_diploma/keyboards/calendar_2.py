import literals
import handlers.lowprice_highprice

from literals import LSTEP
from datetime import timedelta
from telebot.types import CallbackQuery
from create_bot import bot, logger, exception_handler
from telegram_bot_calendar import DetailedTelegramCalendar


def second_date(call: CallbackQuery) -> None:

    """
    Функция запрашивающая у пользователя дату выезда из отеля.
    После запроса для взаимодействия с пользователем создаёт inline-календарь.
    :param call: CallbackQuery
    :return: None
    """

    logger.info(str(call.from_user.id))
    bot.send_message(call.message.chat.id, text=literals.CHECK_OUT)
    calendar, step = DetailedTelegramCalendar(calendar_id=2).build()
    bot.send_message(call.message.chat.id, text=f'{literals.CHOOSE} {LSTEP[step]}', reply_markup=calendar)


@bot.callback_query_handler(func=DetailedTelegramCalendar.func(calendar_id=2))
def cal(call: CallbackQuery) -> None:

    """
    Функция - обработчик inline-календаря. Реагирует только на календарь с id = 2.
    После обработки пользовательской информации, перенаправляет в функцию
    lowprice_highprice.ask_photo.
    :param call: CallbackQuery
    :return: None
    """

    logger.info(str(call.from_user.id))
    with bot.retrieve_data(call.from_user.id, call.message.chat.id) as data:
        result, key, step = DetailedTelegramCalendar(
        min_date=data['date_arrival'] + timedelta(days=1), calendar_id=2, locale='ru').process(call.data)

    if not result and key:
        bot.edit_message_text(f'{literals.CHOOSE} {LSTEP[step]}',
        call.message.chat.id, call.message.message_id, reply_markup=key)

    elif result:
        bot.edit_message_text(f'{literals.SELECTED} {result}',
        call.message.chat.id, call.message.message_id)
        with bot.retrieve_data(call.from_user.id, call.message.chat.id) as data:
            data['date_departure'] = result
        handlers.lowprice_highprice.ask_photo(call)