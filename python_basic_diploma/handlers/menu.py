import literals
import telebot

from telebot import types
from telebot.types import Message
from create_bot import bot, logger, message_exception_handler




bot.set_my_commands([telebot.types.BotCommand(literals.RUN, literals.RESTART)])
@bot.message_handler(commands=literals.START)
@message_exception_handler
def start(message: Message) -> None:

    """
    Функция - главное меню. По команде 'start' приветствует пользователя
    и выводит reply-клавиатуру для дальнейшей работы с тг-ботом.
    :param message: Message
    :return: None
    """

    logger.info(str(message.from_user.id))
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton(literals.HELP)
    btn2 = types.KeyboardButton(literals.LOWPRICE)
    btn3 = types.KeyboardButton(literals.HIGHPRICE)
    btn4 = types.KeyboardButton(literals.BESTDEAL)
    btn5 = types.KeyboardButton(literals.HISTORY)
    markup.add(btn1, btn2, btn3, btn4, btn5)
    bot.send_message(
        message.chat.id, text=literals.GREET.format
        (message.from_user.first_name), reply_markup=markup
    )
    bot.send_message(message.chat.id, text=literals.MANUAL)


