import literals

from telebot import types
from telebot.types import InlineKeyboardMarkup


def keyboard_history() -> InlineKeyboardMarkup:

    """
    Функция - создаёт inline-клавиатуру с меню разделом History.
    :return: InlineKeyboardMarkup
    """

    keyboard = types.InlineKeyboardMarkup(row_width=2)
    view = types.InlineKeyboardButton(text=literals.VIEW_HISTORY, callback_data=literals.VIEW_HISTORY)
    clear = types.InlineKeyboardButton(text=literals.CLEAR_HISTORY, callback_data=literals.CLEAR_HISTORY)
    keyboard.add(view, clear)
    return keyboard


def photo_keyboard() -> InlineKeyboardMarkup:

    """
    Функция - создаёт inline-клавиатуру
    для запроса у пользователя выводить фотографии или нет.
    :return: InlineKeyboardMarkup
    """

    keyboard = types.InlineKeyboardMarkup()
    key_yes = types.InlineKeyboardButton(text=literals.PHOTO_YES, callback_data=literals.PHOTO_YES)
    key_no = types.InlineKeyboardButton(text=literals.PHOTO_NO, callback_data=literals.PHOTO_NO)
    keyboard.add(key_yes, key_no)
    return keyboard


def number_photo_keyboards() -> InlineKeyboardMarkup:

    """
    Функция - создаёт inline-клавиатуру с цифрами на кнопках от 1 до 10.
    Предназначена для запроса информации по количеству фотографий.
    :return: InlineKeyboardMarkup
    """

    keyboard = types.InlineKeyboardMarkup(row_width=5)
    photo_list = []
    for num in literals.NUMBER_PHOTO:
        key = types.InlineKeyboardButton(text=num, callback_data=num)
        photo_list.append(key)
    keyboard.add(
        photo_list[0], photo_list[1], photo_list[2], photo_list[3], photo_list[4],
        photo_list[5], photo_list[6], photo_list[7], photo_list[8], photo_list[9],
    )
    return keyboard