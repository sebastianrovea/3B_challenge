from django.urls import path

from . import views

"""
urls api end points
"""
urlpatterns = [
    path('products', views.create_product, name='create-product'),
    path('inventories/product/<int:product_id>', views.add_stock, name='add-stock'),
    path('orders', views.create_order, name='create-order'),
    path('products/list', views.list_product, name='list-products'),
]
