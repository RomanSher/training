import literals
import config
import sqlite3

from telebot.types import Message, CallbackQuery
from keyboards.inline_keyboards import keyboard_history
from create_bot import bot, logger, message_exception_handler



@message_exception_handler
def history_menu(message: Message) -> None:

    """
    Функция, запускающая команду: 'history'. Выводит пользователю
    меню раздела History в виде inline-кнопок.
    :param message: Message
    :return: None
    """

    logger.info(str(message.from_user.id))
    bot.send_message(
        message.from_user.id, text=literals.HISTORY_MENU, reply_markup=keyboard_history())




@bot.callback_query_handler(func=lambda call: call.data in literals.HISTORY_SELECTION)
@message_exception_handler
def view_or_clear(call: CallbackQuery) -> None:

    """
    Функция - обработчик inline-кнопок. Реагирует только на элементы списка HISTORY_SELECTION.
    В случае выбора пользователем - Просмотреть, выводит клавиатуру с подменю выбора
    режима просмотра истории в БД. В случае выбора пользователем - Очистить, очищает в БД
    историю пользователя и выводит сообщение об успешной очистке.
    :param call: CallbackQuery
    :return: None
    """

    logger.info(str(call.from_user.id))
    bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)
    if call.data == literals.VIEW_HISTORY:
        bot.edit_message_text(
            chat_id=call.message.chat.id, message_id=call.message.message_id,
            text=literals.SHOW_HISTORY
        )
        with sqlite3.connect(config.db, check_same_thread=False) as connect:
            cursor = connect.cursor()
        info = cursor.execute('SELECT * FROM users WHERE user_id =?', (call.from_user.id,))

        if info.fetchone() is None:
            bot.send_message(call.from_user.id, text=literals.EMPTY_STORY)

        else:
            user = (f'SELECT * FROM users WHERE user_id ={call.from_user.id}')
            cursor.execute(user)
            commands = cursor.fetchall()
            command_count = 0
            for _ in commands:
                hotel_count = 0
                bot.send_message(
                    call.from_user.id, text=literals.ENTERED_COMMAND.format(
                        commands[command_count][2],
                        commands[command_count][3]
                    )
                )
                id_hotel = (f'SELECT * FROM hotels WHERE id ={commands[command_count][0]}')
                cursor.execute(id_hotel)
                hotels = cursor.fetchall()
                for _ in hotels:
                    bot.send_message(
                        call.from_user.id, text=literals.RESULT_SEARCH.format(
                            hotels[hotel_count][2],
                            hotels[hotel_count][3],
                            hotels[hotel_count][4],
                            hotels[hotel_count][5],
                            hotels[hotel_count][6]
                        )
                    )
                    hotel_count += 1
                command_count += 1

    elif call.data == literals.CLEAR_HISTORY:

        bot.edit_message_text(
            chat_id=call.message.chat.id, message_id=call.message.message_id,
            text=literals.CLEARED
        )
        with sqlite3.connect(config.db, check_same_thread=False) as connect:
            cursor = connect.cursor()
            user = (f'DELETE FROM users WHERE user_id = {call.from_user.id}')
            cursor.execute(user)
            hotels = (f'DELETE FROM hotels WHERE user_id = {call.from_user.id}')
            cursor.execute(hotels)
            bot.send_message(call.from_user.id, text=literals.CLEANING_IS_COMPLETE)







