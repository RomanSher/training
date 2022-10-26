import literals

from telebot import types
from . help import help_menu
from userstates import UserState
from . history import history_menu
from keyboards.calendar import first_date
from api_rapid.search_address import no_address
from telebot.types import Message, CallbackQuery
from api_rapid.request_photo import photo_search
from api_rapid.request_hotels import hotels_search
from api_rapid.request_city_id import city_id_search
from database.userbase import table_hotels, table_commands
from range_exception import rounding_distance, number_of_days
from create_bot import bot, logger, message_exception_handler
from keyboards.inline_keyboards import photo_keyboard, number_photo_keyboards





@bot.message_handler(state='*', commands=literals.COMMANDS)
@message_exception_handler
def ask_city(message: Message) -> None:

    """
    Функция, запускающая команды:
    'lowprice', 'highprice', 'bestdeal', 'help', 'history'.
    С данной функции осуществляется начало сбора информации по команде,
    для дальнейшего сохранения в базу данных.
    :param message: Message
    :return: None
    """

    logger.info(str(message.from_user.id))
    if message.text == '/help':
        help_menu(message)
    elif message.text == '/history':
        history_menu(message)
    else:
        bot.send_message(
            message.chat.id,
            text=literals.CITY, reply_markup=types.ReplyKeyboardRemove()
        )
        bot.set_state(message.from_user.id, UserState.city, message.chat.id)
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['commands'] = message.text


@bot.message_handler(state=UserState.city)
@message_exception_handler
def check_city(message: Message) -> None:

    """
    Функция, отправляет введенный пользователем город на проверку его наличия.
    Если возвращается int, то запрашивает у пользователя дальнейшую информацию.
    Иначе состояние остается прежним и пользователю будут предложено
    повторно ввести город.
    :param message: Message
    :return: None
    """

    logger.info(str(message.from_user.id))
    city_id = city_id_search(message, message.text)
    if type(city_id) == int:
        bot.send_message(message.chat.id, text=literals.NUMBER_HOTELS)
        bot.set_state(message.from_user.id, UserState.hotel, message.chat.id)
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['city_id'] = city_id


@bot.message_handler(state=UserState.hotel, is_digit=True)
@message_exception_handler
def ask_hotel(message: Message) -> None:

    """
    Функция, реагирует только на положительные целые числа. Если начальная команда
    введенная пользователем равна 'bestdeal', то запрашиваем у пользователя
    информацию о диапазоне цен переходя в файл 'bestdeal.py', функцию 'min_price'
    Если команда равна 'lowprice', или 'highprice', присваиваем дефолтные
    значения и переходим в файл calendar.py.
    :param message: Message
    :return: None
    """

    logger.info(str(message.from_user.id))
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['number_of_hotels'] = message.text
    if data['commands'] == literals.BESTDEAL:
        data['price'] = literals.LOWEST_PRICE
        bot.send_message(message.from_user.id, text=literals.MIN_PRICE)
        bot.set_state(message.from_user.id, UserState.minPrice, message.chat.id)
    else:
        if data['commands'] == literals.LOWPRICE:
            data['price'] = literals.LOWEST_PRICE
        elif data['commands'] == literals.HIGHPRICE:
            data['price'] = literals.HIGHEST_PRICE
        data['min_hotel_price'] = 0
        data['max_hotel_price'] = 10000000
        data['min_dist_center'] = 0
        data['max_dist_center'] = 1000
        bot.send_message(message.from_user.id, text=literals.CHECK_IN)
        first_date(message)


@bot.message_handler(state=UserState.filter, is_digit=False)
@message_exception_handler
def incorrect_number_input(message):

    """
    Функция вызывается в случае некорректного ввода пользователем
    числовых значений. Состояние остается прежним, а пользователю
    предложено ввести информацию повторно.
    :param message: Message
    :return: None
    """

    logger.info(str(message.from_user.id))
    bot.send_message(message.chat.id, text=literals.NUMBER_ERROR)



@message_exception_handler
def ask_photo(message: Message) -> None:

    """
    Функция - уточняющая у пользователя необходимость вывода
    фотографий к отелям, в формате inline-кнопок.
    :param message: Message
    :return: None
    """

    logger.info(str(message.from_user.id))
    bot.send_message(
        message.from_user.id, text=literals.UPLOADING_PHOTOS,
        reply_markup=photo_keyboard()
    )
    bot.set_state(message.from_user.id, UserState.photo)



@bot.callback_query_handler(func=lambda call: call.data in literals.PHOTO_SELECTION)
@bot.message_handler(state=UserState.photo)
@message_exception_handler
def ask_number_of_photos(call: CallbackQuery) -> None:

    """
    Функция - обработчик inline-кнопок. Реагирует только на информацию входящую
    в список 'PHOTO_SELECTION'. В случае положительного ответа, запрашивает информацию
    о количестве фотографий для вывода, в формате inline-кнопок.
    Если полученный ответ отрицательный, то отправляет далее по сценарию в функцию
    'ending'.
    :param call: CallbackQuery
    :return: None
    """

    logger.info(str(call.from_user.id))
    bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)
    if call.data == literals.PHOTO_YES:
        with bot.retrieve_data(call.from_user.id, call.message.chat.id) as data:
            data['flag_photo'] = True
        bot.edit_message_text(
            chat_id=call.message.chat.id, message_id=call.message.message_id,
            text=literals.WITH_PHOTOS
        )
        bot.send_message(
            call.from_user.id, text=literals.NUMBER_OF_PHOTOS,
            reply_markup=number_photo_keyboards()
        )
        bot.set_state(call.from_user.id, UserState.sending)
    elif call.data == literals.PHOTO_NO:
        with bot.retrieve_data(call.from_user.id, call.message.chat.id) as data:
            data['flag_photo'] = False
        bot.edit_message_text(
            chat_id=call.message.chat.id, message_id=call.message.message_id,
            text=literals.WITHOUT_PHOTOS
        )
        ending(call)


@bot.callback_query_handler(func=lambda call: call.data in literals.CALL_NUMBER_PHOTO)
@bot.message_handler(state=UserState.sending)
@message_exception_handler
def transition(call: CallbackQuery) -> None:

    """
    Функция - обработчик inline-кнопок. Реагирует только на запросы о количестве фотографий.
    :param call: CallbackQuery
    :return: None
    """

    logger.info(str(call.from_user.id))
    bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)
    with bot.retrieve_data(call.from_user.id, call.message.chat.id) as data:
        data['number_of_photos'] = call.data
        bot.edit_message_text(
            chat_id=call.message.chat.id, message_id=call.message.message_id,
            text=literals.SHOWING_PHOTOS.format(data['number_of_photos'])
        )
    ending(call)


@message_exception_handler
def ending(call: CallbackQuery) -> None:

    """
    Функция оповещает пользователя о начале поиска. Делает запрос к API
    (request_property_list). Далее с результатом из API осуществляется
    переход в функцию 'search_attributes'.
    :param call: CallbackQuery
    :return: None
    """

    logger.info(str(call.from_user.id))
    bot.send_message(call.from_user.id, text=literals.STARTING_SEARCH)
    hotels_search(call)
    search_attributes(call)



@message_exception_handler
def search_attributes(call: CallbackQuery) -> None:

    """
    Функция - обрабатывающая ответ с API. Если статус код успешный, то создаётся запись в БД,
    о команде пользователя и результатах поиска. Если необходимо, вызывается функция
    request_photo.py. Результат поиска отелей выводится пользователю.
    :param call: CallbackQuery
    :return: None
    """

    logger.info(str(call.from_user.id))
    with bot.retrieve_data(call.from_user.id, call.message.chat.id) as data:
        data['hotel_json'] = data['city_json']['data']['body']['searchResults']['results']
        command_id = table_commands(call.from_user.id, data['commands'])
        number_of_available = len(data['hotel_json'])
        output = 0

        for num in range(number_of_available):
            distance = rounding_distance(num, data['hotel_json'])
            if int(data['min_dist_center']) <= distance <= int(data['max_dist_center']) \
                    and output < int(data['number_of_hotels']):
                landmarks = data['hotel_json'][num]['landmarks'][0]['distance']
                current = data['hotel_json'][num]['ratePlan']['price']['current']
                id_hotel = data['hotel_json'][num]['id']
                name = data['hotel_json'][num]['name']
                address = no_address(num, data['hotel_json'])
                full_price = number_of_days(call, current)
                table_hotels(command_id, call.from_user.id, name,
                            address, landmarks, current, full_price)
                HEADER_HOTEL = literals.RESULT_SEARCH.format(
                    name, address, landmarks, current, full_price
                )
                if data['flag_photo']:
                    medias = photo_search(call, id_hotel, HEADER_HOTEL)
                    bot.send_media_group(call.message.chat.id, medias)
                else:
                    bot.send_message(call.message.chat.id, HEADER_HOTEL)
                output += 1
        bot.send_message(
            call.message.chat.id, text=literals.RESULT.format
            (output, data['number_of_hotels'])
        )
    bot.delete_state(call.from_user.id, call.message.chat.id)
