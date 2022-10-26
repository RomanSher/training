import json
import config
import requests

from telebot.types import CallbackQuery
from create_bot import bot, logger, exception_handler


@exception_handler
def hotels_search(call: CallbackQuery) -> None:

    """
    Функция - делающая запрос на API по адресу: 'https://hotels4.p.rapidapi.com/properties/list'
    В зависимости от введенной команды сортирует отели по возврастанию цены, по убыванию или же
    по введенному диапазону, а также по удаленности отеля от центра города.
    :param call: CallbackQuery
    :return: None
    """

    logger.info(str(call.from_user.id))
    with bot.retrieve_data(call.from_user.id, call.message.chat.id) as data:

        url = config.url_list
        querystring = {
            'destinationId': data['city_id'],
            'pageNumber': '1',
            'pageSize': '25',
            'checkIn': data['date_arrival'],
            'checkOut': data['date_departure'],
            'adults1': '1',
            'priceMin': data['min_hotel_price'],
            'priceMax': data['max_hotel_price'],
            'sortOrder': data['price'],
            'locale': 'ru_RU',
            'currency': 'RUB'
            }

    response = requests.request("GET", url, headers=config.client, params=querystring)
    data_response = response.text
    data['city_json'] = json.loads(data_response)





















