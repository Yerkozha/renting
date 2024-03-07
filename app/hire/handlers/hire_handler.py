
from app.hire.models import ProductModel, OrderModel, OrderedProduct
from datetime import datetime
from rest_framework import exceptions, status

class ServiceErrorException(exceptions.APIException):
    status_code = status.HTTP_400_BAD_REQUEST


class HireHandler(): # mixins additional fields

    def __init__(self):
        pass

    def create_order(self, order_input, product):

        existence = OrderedProduct.objects.filter(product=product).exists()
        if existence:
            raise ServiceErrorException("Product has been already hired")

        delta = order_input.end - order_input.start
        order = OrderModel.objects.create(start=order_input.start, end=order_input.end, total_price=product.price * delta.days)
        ordered_product = OrderedProduct.objects.create(order=order, product=product, duration=delta.days)

        return ordered_product

    def create_product(self, product_input):

        product = ProductModel.objects.create(name=product_input.name, price=product_input.price)
        return product