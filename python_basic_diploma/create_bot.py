"""
Файл для создания экземпляров бота.
Также добавляет пользовательские фильтры
и содержит декоратор для отлова исключений и логгирования ошибок.
"""

import telebot
import config
import literals

from typing import Callable
from telebot.types import Message
from telebot import custom_filters
from logging_config import custom_logger
from telebot.storage import StateMemoryStorage


storage = StateMemoryStorage()
bot = telebot.TeleBot(config.TOKEN, state_storage=storage)
bot.add_custom_filter(custom_filters.StateFilter(bot))
bot.add_custom_filter(custom_filters.IsDigitFilter())
logger = custom_logger('bot_logger')




def message_exception_handler(func: Callable) -> Callable:

    """
    Декоратор - оборачивающий функцию в try-except блок.
    :param func: Callable
    :return: Callable
    """

    def wrapped_func(message: Message) -> Callable:
        try:
            result = func(message)
            return result
        except Exception as error:
            logger.error(literals.LOG_ERROR, exc_info=error)
            bot.send_message(message.chat.id, text=literals.ERROR)
    return wrapped_func

def exception_handler(func: Callable) -> Callable:

    """
    Декоратор - оборачивающий функцию в try-except блок.
    :param func: Callable
    :return: Callable
    """

    def wrapped_func(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            return result
        except Exception as error:
            logger.error(literals.LOG_ERROR, exc_info=error)

    return wrapped_func
