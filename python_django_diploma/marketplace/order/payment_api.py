import json
import logging
import os
from typing import Dict

import requests
from order.models import PaymentTransaction, Order


logger = logging.getLogger('payment_handler')


class PaymentApi:
    _PAYMENT_API_HOST = os.environ.get('PAYMENT_API_HOST', 'localhost')
    _PAYMENT_API_PORT = os.environ.get('PAYMENT_API_PORT', '5000')
    _API_URL = f'http://{_PAYMENT_API_HOST}:{_PAYMENT_API_PORT}/pay'
    _HEADERS = {'Content-Type': 'application/json'}

    def __init__(self, data: Dict) -> None:
        """
        Инициализирует атрибуты объекта.
        :param data: Данные, которые будут использоваться для инициализации объекта.
        :return: None.
        """
        self._number = data['number']
        self._name = data['name']
        self._month = data['month']
        self._year = data['year']
        self._code = data['code']
        self._order_id = data['order_id']
        self._user_id = data['user_id']

    def process(self) -> None:
        """
        Метод отправляет запрос на фиктивный сервис оплаты для проведения платежа.
        :return: None.
        """
        data = {
            'number': self._number,
            'month': self._month,
            'year': self._year,
            'code': self._code,
            'name': self._name,
        }
        try:
            response = requests.post(self._API_URL, data=json.dumps(data), headers=self._HEADERS)
        except Exception as error:
            logger.error(f'[PAYMENT_ERROR]: order_id: {self._order_id}, error_message: {error}')
            return
        self.payment_callback(response)

    def payment_callback(self, response) -> None:
        """
        Обработка ответа от фиктивного платежного сервиса.
        :param response: Ответ от фиктивного платежного сервиса.
        :return: None.
        """
        payment = PaymentTransaction.objects.create(
            uuid=response.json().get('uuid'),
            order_id=self._order_id,
            user_id=self._user_id
        )
        if response.status_code == 200:
            payment.status = PaymentTransaction.COMPLETED
            payment.order.status = Order.PAID
            payment.order.save()
            payment.save()
            logger.info(
                f'payment was successful. '
                f'id:{payment.id}, '
                f'uuid:{payment.uuid}'
            )
        else:
            payment.status = PaymentTransaction.ERROR
            payment.error_message = response.json().get('error_message')
            payment.save()
            logger.info(
                f'payment error. '
                f'id:{payment.id}, '
                f'uuid:{payment.uuid}, '
                f'error_message:{payment.error_message}'
            )
