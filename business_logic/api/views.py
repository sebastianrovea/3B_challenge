import traceback

from django.http import JsonResponse

from rest_framework.decorators import api_view

from ..models import Product, Order, OrderLine

from ..dao.product import ProductDB
from ..dao.order import OrderDB

from ..utils.loggers import log
from ..utils.const import ErrorMessage, SuccessMessage, ProductError


@api_view(['POST'])
def create_product(request):
    """
    create_product logic to create a new method
    """
    try:
        log.info("create_product logic api method")
        if request.method == 'POST':
            data = request.data
            exist_product = ProductDB.exist_by_sku(data.get("sku"))
            if exist_product:
                return JsonResponse({"message": ErrorMessage.PRODUCT_EXIST.value}, status=400)
            if data.get("sku") and data.get("name"):
                product = Product(
                    sku=data.get("sku"),
                    name=data.get("name"),
                    description=data.get("description", ""),
                    stock=int(data.get("stock", 100))
                )
                product_id = ProductDB.create_product(product)
                return JsonResponse(
                    {"message": SuccessMessage.CREATED.value, "product_id": product_id},
                    status=200
                )
            else:
                return JsonResponse({"message": ErrorMessage.NECESARY_PARAMS.value}, status=400)
    except ProductError as pr_e:
        log.error("create prodcut api error: {}".format(pr_e))
        return JsonResponse(
            {"message": ErrorMessage.DATABASE_ERROR.value}, status=500
        )
    except Exception as e:
        log.error("create prodcut api error: {}".format(e))
        return JsonResponse(
            {"message": ErrorMessage.INTERNAL_ERROR.value}, status=500
        )


@api_view(['PATCH'])
def add_stock(request, product_id):
    """
    add_stock logic method to add stock to a product
    """
    try:
        log.info("add_stock logic api method")
        if request.method == 'PATCH':
            data = request.data
            if "stock" not in data or int(data.get("stock")) <= 0:
                return JsonResponse(
                    {"message": ErrorMessage.STOCK_PARAMS.value},
                    status=400
                )
            exist_product = ProductDB.exist(product_id)
            if exist_product:
                ProductDB.edit_field_prodcut(id=product_id, stock=int(data.get("stock")))
                return JsonResponse(
                    {"message": SuccessMessage.UPDATE.value, "product_id": product_id},
                    status=200
                )
            return JsonResponse(
                {"message": ErrorMessage.UNEXISTENT_PRODCUT.value}, status=404
            )
    except ProductError as pr_e:
        log.error("create prodcut api error: {}".format(pr_e))
        return JsonResponse(
            {"message": ErrorMessage.DATABASE_ERROR.value}, status=500
        )
    except Exception as e:
        return JsonResponse(
            {"message": ErrorMessage.INTERNAL_ERROR.value}, status=500
        )
    

@api_view(['POST'])
def create_order(request):
    """
    create_order logic method to create a new order of product
    """
    try:
        log.info("create_order logic api method")
        if request.method == 'POST':
            data = request.data
            if data.get("order_line_object") and data.get("client"):
                order_line_object = data.get("order_line_object")
                for key, value in order_line_object.items():
                    product = ProductDB.get_product_from_sku(key)
                    if not product:
                        return JsonResponse(
                            {"message": ErrorMessage.UNEXISTENT_PRODCUT.value, "sku": key}, status=404
                        )
                    if int(value) > product.get("stock"):
                        return JsonResponse(
                            {"message": ErrorMessage.NO_STOCK.value, "sku": key}, status=404
                        )
                order = Order(
                    client = data.get("client")
                )
                order_id = OrderDB.create_order(order)
                for key, value in order_line_object.items():
                    product = ProductDB.get_product_from_sku(key)
                    order_line = OrderLine(
                        order_id = int(order_id),
                        product_id = product.get("id"),
                    )
                    OrderDB.create_order_line(order_line)
                    ProductDB.edit_field_prodcut(id=product.get("id"), stock=value, sub=True)
                return JsonResponse(
                    {"message": SuccessMessage.SUCCESS.value}, status=200
                )
            else:
                return JsonResponse({"message": ErrorMessage.NECESARY_PARAMS.value}, status=400)

    except ProductError as pr_e:
        log.error("create order api error: {}".format(pr_e))
        return JsonResponse(
            {"message": ErrorMessage.DATABASE_ERROR.value}, status=500
        )
    except Exception as e:
        log.error("raceback:",traceback.format_exc())
        log.error("create order api error: {}".format(e))
        return JsonResponse(
            {"message": ErrorMessage.INTERNAL_ERROR.value}, status=500
        )


@api_view(['GET'])
def list_product(request):
    """
    list_product method to list all product
    """
    try:
        log.info("list_product logic api method")
        if request.method == 'GET':
            products = ProductDB.list_all()
            return JsonResponse(
                {"Product list:": products}, status=200
            )
    except ProductError as pr_e:
        log.error("create prodcut api error: {}".format(pr_e))
        return JsonResponse(
            {"message": ErrorMessage.DATABASE_ERROR.value}, status=500
        )
    except Exception as e:
        return JsonResponse(
            {"message": ErrorMessage.INTERNAL_ERROR.value}, status=500
        )
