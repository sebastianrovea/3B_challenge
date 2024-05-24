import traceback

from django.forms.models import model_to_dict

from ..models import Product
from ..utils.loggers import log
from ..utils.const import ProductError


class ProductDB:

    @classmethod
    def exist(cls, id: int) -> bool:
        """
        exit method to valid if this sku exist or not
        """
        try:
            log.info("exist method")
            count = Product.objects.filter(id=id).count()
            if count > 0:
                return True
            return False

        except Exception as e:
            log.error("exist method error: {}".format(e))
            raise ProductError("Problem to valid if thiss prodcut exist or not")
        
    @classmethod
    def exist_by_sku(cls, sku: str) -> bool:
        """
        exit method to valid if this sku exist or not
        """
        try:
            log.info("exist by sku method")
            count = Product.objects.filter(sku=sku).count()
            if count > 0:
                return True
            return False

        except Exception as e:
            log.error("exist by sku method error: {}".format(e))
            raise ProductError("Problem to valid if thiss prodcut exist or not")

    @classmethod
    def list_all(cls) -> list:
        """
        list_all method to list all product
        """
        try:
            log.info("list all method")
            products = Product.objects.all()
            return list(products.values())

        except Exception as e:
            log.error("list all method error: {}".format(e))
            raise ProductError("Problem to list product")

    @classmethod
    def get_product(cls, id) -> dict:
        """
        get_product method to retrieve a product
        """
        try:
            log.info("get product method")
            product = Product.objects.get(id=id)
            return model_to_dict(product)

        except Exception as e:
            log.error("get product method error: {}".format(e))
            raise ProductError("Problem to get product")
        
    @classmethod
    def get_product_from_sku(cls, sku) -> dict:
        """
        get_product method to retrieve a product
        """
        try:
            log.info("get product method")
            product = Product.objects.get(sku=sku)
            return model_to_dict(product)

        except Exception as e:
            log.error("Traceback:", traceback.format_exc())
            log.error("get product by sku method error: {}".format(e))
            raise ProductError("Problem to get product")

    @classmethod
    def create_product(cls, product: Product) -> int:
        """
        create_product method to save a new product
        """
        try:
            log.info("Create product method")
            product.save()
            return product.id

        except Exception as e:
            log.error("create prodcut method error: {}".format(e))
            raise ProductError("Problem to create product")
        
    @classmethod
    def edit_field_prodcut(cls, **kwargs):
        """
        edit_field_prodcut method to edit any values of prodcut class
        """
        try:
            object_value = {}
            for key, value in kwargs.items():
                object_value[key] = value
            product = Product.objects.get(id=object_value.get("id"))
            if "stock" in object_value:
                if object_value.get("sub"):
                    product.stock -= int(object_value.get("stock"))
                else:
                    product.stock += int(object_value.get("stock"))
            product.save()
            return True
        except Exception as e:
            log.error("edit field product method error: {}".format(e))
            raise ProductError("Problem to edit product")