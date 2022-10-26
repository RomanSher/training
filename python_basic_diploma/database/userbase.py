import config
import sqlite3
import datetime

from create_bot import exception_handler


@exception_handler
def table_commands(user_id: int, commands: str) -> int:

    """
    Функция записывает в БД (Users.db): user_id пользователя, запрашиваемую команду по поиску
    отеля и время запроса, а также возвращает id записи в БД для взаимодействия
    с таблицей отелей.
    :param user_id: int
    :param commands: str
    :return: int
    """

    dt_obj = datetime.datetime.now()
    dt_string = dt_obj.strftime('%d-%b-%Y %H:%M:%S')
    with sqlite3.connect(config.db, check_same_thread=False) as connect:
        cursor = connect.cursor()
        cursor.execute(
            'INSERT INTO users (user_id, commands, date) VALUES (?, ?, ?)',
            (user_id, commands, dt_string)
        )
        connect.commit()

        sqlite_select_query = ("SELECT `id` FROM users order by `id` desc limit 1;")
        cursor.execute(sqlite_select_query)
        record = cursor.fetchall()
        return record[0][0]


@exception_handler
def table_hotels(command_id: int, user_id: int, name: str, address: str,
                landmarks: str, current: str, full_price: str) -> None:

    """
    Функция записывает в БД (Users.db) атрибуты отеля, а также id команды для взаимодействия
    с таблицей пользователей.
    :param command_id: int
    :param user_id: int
    :param name: str
    :param address: str
    :param landmarks: str
    :param current: str
    :param full_price: str
    :return: None
    """

    with sqlite3.connect(config.db, check_same_thread=False) as connect:
        cursor = connect.cursor()
        cursor.execute(
            'INSERT INTO hotels (id, user_id, name_hotel, address, distance, '
            'price_day, price) VALUES (?, ?, ?, ?, ?, ?, ?)',
            (command_id, user_id, name, address, landmarks, current, full_price)
        )
        connect.commit()



