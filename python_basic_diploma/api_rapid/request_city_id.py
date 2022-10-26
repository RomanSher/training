import requests
import json
import literals
import config
import create_bot

from typing import Union
from telebot.types import Message
from create_bot import bot, logger, exception_handler


@exception_handler
def city_id_search(message: Message, city: str) -> Union[bool, int]:

    """
    Функция - делающая запрос на API по адресу: 'https://hotels4.p.rapidapi.com/locations/search'
    Если введенный город удалось найти, то возвращает id города. В противном случае возвращает
    bool.
    :param message: Message
    :param city: str
    :return: Union[bool, int]
    """

    logger.info(str(message.from_user.id))
    create_bot.bot.send_message(message.from_user.id, text=literals.AVAILABILITY_CITY)
    querystring = {
        'query': city,
        'locale': 'ru_RU'
    }

    response = requests.request("GET", config.url, headers=config.client, params=querystring)
    data = response.text
    data_json = json.loads(data)
    check_city = data_json['suggestions'][0]['entities']

    if check_city == []:
        bot.send_message(message.chat.id, text=literals.INCORRECT_CITY)
        return False
    else:
        city_id = data_json['suggestions'][0]['entities'][0]['destinationId']
        bot.send_message(message.chat.id, text=literals.CORRECT_CITY)
        return int(city_id)