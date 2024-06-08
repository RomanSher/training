from datetime import datetime
import uuid
from typing import Dict

from app import db


class Payment(db.Model):
    COMPLETED = 'COMPLETED'
    ERROR = 'ERROR'

    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String(36), unique=True, nullable=False, default=lambda: str(uuid.uuid4()))
    create_at = db.Column(db.DateTime, default=datetime.utcnow)
    number = db.Column(db.Integer, nullable=False)
    month = db.Column(db.Integer, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    code = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(20), default=COMPLETED)
    error_message = db.Column(db.String(100), nullable=True)

    def __repr__(self):
        return f'<payment {self.id}>'

    @staticmethod
    def create_payment(data: Dict, status: str, error_message: str) -> 'Payment':
        """
        Создает оплату.
        :param data: Словарь с данными, необходимыми для создания оплаты.
        :param status: Строковое значение статуса оплаты.
        :param error_message: Строковое значение сообщение об ошибке.
        :return: Созданный экземпляр оплаты.
        """
        payment = Payment(
            number=data['number'],
            month=data['month'],
            year=data['year'],
            code=data['code'],
            name=data['code'],
            status=status,
            error_message=error_message
        )
        db.session.add(payment)
        db.session.commit()

        return payment
