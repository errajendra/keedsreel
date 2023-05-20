from . import client


def create_order(amount, currency, receipt=None):
    data = {"amount": amount, "currency": currency, "receipt": receipt}
    payment = client.order.create(data=data)
    return payment
