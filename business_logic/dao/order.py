from ..models import Order, OrderLine
from ..utils.loggers import log
from ..utils.const import ProductError


class OrderDB:

    @classmethod
    def create_order(cls, order: Order) -> int:
        """
        create_order method to save a new order line
        """
        try:
            log.info("Create order method")
            order.save()
            return order.id

        except Exception as e:
            log.error("create order method error: {}".format(e))
            raise ProductError("Problem to create order")


    @classmethod
    def create_order_line(cls, order_line: OrderLine) -> int:
        """
        create_order_line method to save a new order line
        """
        try:
            log.info("Create order line method")
            order_line.save()
            return order_line.id

        except Exception as e:
            log.error("create order line method error: {}".format(e))
            raise ProductError("Problem to create order line")