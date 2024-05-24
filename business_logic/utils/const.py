"const file"

from enum import Enum

class ErrorMessage(Enum):
    """
    Error messages class for the program
    """
    PRODUCT_EXIST = "This product already exist"
    NECESARY_PARAMS = "Some params are mandatory"
    STOCK_PARAMS = "stock params must be sent and it must be greater than zero"
    DATABASE_ERROR = "Database error"
    INTERNAL_ERROR = "Internal error"
    UNEXISTENT_PRODCUT = "This product does not exist"
    NO_STOCK = "Insufficient stock"


class SuccessMessage(Enum):
    CREATED = "Product created successfully"
    UPDATE = "Product updated successfully"
    SUCCESS = "Success operation"


class ProductError(Exception):
    """Personalized Error for Product dao"""
    pass
