# inventory_app/jobs.py
from ..models import Product


def check_stock():
    print("Starting job to check lower stock")
    low_stock_products = Product.objects.filter(stock__lt=10)
    for product in low_stock_products:
        print(f"Alert: Product {product.name} has lower stock ({product.stock})")
