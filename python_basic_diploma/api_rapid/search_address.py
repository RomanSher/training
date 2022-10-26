from create_bot import exception_handler


@exception_handler
def no_address(num: int, hotel_json: dict) -> str:

    """
    Функция проверяет указана ли улица расположения отеля и возвращает её.
    В противном случае возвращает регион.
    :param num: int
    :param hotel_json: dict
    :return: str
    """

    data_address = hotel_json[num]['address']
    for street in data_address:
        if street == 'streetAddress':
            address = hotel_json[num]['address']['streetAddress']
            return address
        else:
            address = hotel_json[num]['address']['region']
            return address