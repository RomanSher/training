import json
import config
import requests

from telebot.types import InputMediaPhoto, CallbackQuery
from create_bot import bot, logger, exception_handler


@exception_handler
def photo_search(call: CallbackQuery, id_hotel: int, HEADER_HOTEL: str) -> list:

    """
    Функция - делающая запрос на API по адресу:
    'https://hotels4.p.rapidapi.com/properties/get-hotel-photos'
    Вызывается при необходимости вывода фотографий к отелям. Возвращает List,
    содержащий в себе список фотографий отелей.
    :param call: CallbackQuery
    :param id_hotel: int
    :param HEADER_HOTEL: str
    :return: List
    """

    logger.info(str(call.from_user.id))
    url = config.url_photos
    querystring = {
        'id': id_hotel
    }

    response = requests.request('GET', url, headers=config.client, params=querystring)
    data = response.text
    data_photo = json.loads(data)

    with bot.retrieve_data(call.from_user.id, call.message.chat.id) as data:
        number_of_available = len(data_photo['hotelImages'])
        number_of_possible = min(int(data['number_of_photos']), number_of_available)
        medias = []
        count = 0
        for number in range(number_of_possible):
            result = data_photo['hotelImages'][number]['baseUrl']
            photo = result.replace('{size}', 'z')
            count += 1
            medias.append(
                InputMediaPhoto(photo, caption=HEADER_HOTEL
                if count == 1 else '', parse_mode='Markdown')
            )
        return medias