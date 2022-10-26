import literals

from telebot.types import Message
from create_bot import bot, logger, message_exception_handler



@message_exception_handler
def help_menu(message: Message) -> None:

    """
    Функция, запускающая команду: 'help'.
    Выводит инстукцию для работы с тг-ботом и описание команд.
    :param message: Message
    :return: None
    """

    logger.info(str(message.from_user.id))
    bot.send_message(message.chat.id, text=literals.HELP_INFO)



