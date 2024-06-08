from flask import request, jsonify
from flask_marshmallow import Marshmallow
from marshmallow import fields

from constants import (
    REQUIRED_CARD_NUMBER, REQUIRED_MONTH, REQUIRED_YEAR,
    REQUIRED_CODE, REQUIRED_NAME, INVALID_CARD_DATE,
    PAYMENT_NOT_FOUND
)
from utils import check_date, check_length, random_error
from flask import Blueprint


app_route = Blueprint('route', __name__)
ma = Marshmallow()


class PaymentSchema(ma.Schema):
    number = fields.Int(required=True, help=REQUIRED_CARD_NUMBER)
    month = fields.Int(required=True, help=REQUIRED_MONTH)
    year = fields.Int(required=True, help=REQUIRED_YEAR)
    code = fields.Int(required=True, help=REQUIRED_CODE)
    name = fields.Str(required=True, help=REQUIRED_NAME)


@app_route.route('/pay', methods=['POST'])
def process_payment():
    from models import Payment
    data = request.json
    errors = PaymentSchema().validate(data)
    length_error = check_length(data)
    error_message = ''
    if errors or length_error:
        error_message = errors or length_error
        return jsonify({'error_message': error_message}), 400

    if check_date(data.get('month'), data.get('year')):
        return jsonify({'error_message': INVALID_CARD_DATE}), 400

    if int(data.get('number')) % 2 == 0 and int(data.get('number')) % 10 != 0:
        status = Payment.COMPLETED
    else:
        status = Payment.ERROR
        error_message = random_error()

    payment = Payment.create_payment(data, status, error_message)

    response = {
        'uuid': payment.uuid,
        'status': payment.status,
        'error_message': payment.error_message
    }
    if status == Payment.COMPLETED:
        return jsonify(response), 200
    else:
        return jsonify(response), 500


@app_route.route('/pay', methods=['GET'])
def get_payment():
    from models import Payment
    uuid = request.json.get('uuid')
    payment = Payment.query.filter_by(uuid=uuid).first()
    if payment:
        response = {
            'uuid': payment.uuid,
            'status': payment.status,
            'error_message': payment.error_message
        }
        return jsonify(response), 200
    else:
        return jsonify({'error_message': PAYMENT_NOT_FOUND}), 404
