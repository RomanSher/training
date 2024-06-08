from celery import shared_task

from order.payment_api import PaymentApi


@shared_task
def process_payment(data):
    payment_api = PaymentApi(data)
    payment_api.process()
