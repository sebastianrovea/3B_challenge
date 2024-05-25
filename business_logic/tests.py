from django.test import TestCase

from unittest import mock

from .models import Product, Order, OrderLine

from .utils.const import ProductError, OrderError

from .dao.order import OrderDB
from .dao.product import ProductDB

class ModelsTestCase(TestCase):

    def test_new_product(self):
        product = Product(
            sku="sku_test",
            name="Test product",
            description="some description test",
            stock=200
        )
        self.assertEqual(product.sku, 'sku_test')
        self.assertEqual(product.stock, 200)
        self.assertEqual(product.description, 'some description test')
        self.assertEqual(product.stock, 200)

    def test_new_order(self):
        order = Order(
            client="Test client"
        )
        self.assertEqual(order.client, 'Test client')

    def test_new_order_line(self):
        order_line = OrderLine(
            order_id=10,
            product_id=20
        )
        self.assertEqual(order_line.order_id, 10)
        self.assertEqual(order_line.product_id, 20)

class DaoOrderTestCase(TestCase):
    
    def test_create_order(self):
        order = Order.objects.create(client="Test client")
        result = OrderDB.create_order(order)
        self.assertTrue(result)

    @mock.patch('business_logic.models.Order.save')
    def test_create_order_failes(self, mock_save):
        order = Order()
        mock_save.side_effect = Exception('Test error')

        with self.assertRaises(OrderError):
            OrderDB.create_order(order)

    def test_create_order_line(self):
        order_line = OrderLine.objects.create(
            order_id=10,
            product_id=20
        )
        result = OrderDB.create_order_line(order_line)
        self.assertTrue(result)

    @mock.patch('business_logic.models.Order.save')
    def test_create_order_line_failes(self, mock_save):
        order_line = OrderLine()
        mock_save.side_effect = Exception('Test error')

        with self.assertRaises(OrderError):
            OrderDB.create_order(order_line)


class DaoProductTestCase(TestCase):
    
    @mock.patch('business_logic.models.Product.objects.filter')
    def test_exist_true(self, mock_filter):
        id = 1
        mock_filter.return_value.count.return_value = 1

        result = ProductDB.exist(id)

        self.assertTrue(result)

    @mock.patch('business_logic.models.Product.objects.filter')
    def test_exist_false(self, mock_filter):
        id = 1
        mock_filter.return_value.count.return_value = 0

        result = ProductDB.exist(id)

        self.assertFalse(result)

    @mock.patch('business_logic.models.Product.objects.filter')
    def test_exist_failed(self, mock_filter):
        id = 1
        mock_filter.side_effect = Exception('Test error')

        with self.assertRaises(ProductError):
            ProductDB.exist(id)

    @mock.patch('business_logic.models.Product.objects.filter')
    def test_exist_by_sku_true(self, mock_filter):
        id = 1
        mock_filter.return_value.count.return_value = 1

        result = ProductDB.exist_by_sku(id)

        self.assertTrue(result)

    @mock.patch('business_logic.models.Product.objects.filter')
    def test_exist_by_sku_false(self, mock_filter):
        id = 1
        mock_filter.return_value.count.return_value = 0

        result = ProductDB.exist_by_sku(id)

        self.assertFalse(result)

    @mock.patch('business_logic.models.Product.objects.filter')
    def test_exist_by_sku_failed(self, mock_filter):
        id = 1
        mock_filter.side_effect = Exception('Test error')

        with self.assertRaises(ProductError):
            ProductDB.exist_by_sku(id)

    @mock.patch('business_logic.models.Product.objects.all')
    def test_list_all(self, mock_all):
        products_data = [
            {'id': 1, 'sku': 'sku1', 'name': 'Product 1', 'stock': 100},
            {'id': 2, 'sku': 'sku2','name': 'Product 2', 'stock': 150}
        ]
        mock_all.return_value.values.return_value = products_data

        products = ProductDB.list_all()

        self.assertEqual(products, products_data)

    @mock.patch('business_logic.models.Product.objects.all')
    def test_list_all_failed(self, mock_all):
        mock_all.side_effect = Exception('Test error')

        with self.assertRaises(ProductError):
            ProductDB.list_all()

    @mock.patch('business_logic.models.Product.objects.get')
    def test_get_product(self, mock_get):
        id = 1
        product_data = {'id': 1, 'name': 'Product 1', 'sku': 'sku1'}
        mock_get.return_value = Product(**product_data)

        product = ProductDB.get_product(id)

        expected_response = {
            'id': 1, 'sku': 'sku1', 'name': 'Product 1', 'description': None, 'stock': 100
        }
        self.assertEqual(product, expected_response)

    @mock.patch('business_logic.models.Product.objects.get')
    def test_get_product_error(self, mock_get):
        id = 1
        mock_get.side_effect = Exception('Test error')

        with self.assertRaises(ProductError):
            ProductDB.get_product(id)

    @mock.patch('business_logic.models.Product.objects.get')
    def test_get_product_from_sku(self, mock_get):
        sku = "sku1"
        product_data = {'id': 1, 'name': 'Product 1', 'sku': 'sku1'}
        mock_get.return_value = Product(**product_data)

        product = ProductDB.get_product_from_sku(sku)

        expected_response = {
            'id': 1, 'sku': 'sku1', 'name': 'Product 1', 'description': None, 'stock': 100
        }
        self.assertEqual(product, expected_response)

    @mock.patch('business_logic.models.Product.objects.get')
    def test_get_product_from_sku_error(self, mock_get):
        sku = "sku1"
        mock_get.side_effect = Exception('Test error')

        with self.assertRaises(ProductError):
            ProductDB.get_product_from_sku(sku)

    def test_create_product(self):
        product = Product.objects.create(
            name='Product 1', sku='sku1', description='Description 1', stock=100
        )
        result = ProductDB.create_product(product)
        self.assertTrue(result)

    @mock.patch('business_logic.models.Product.save')
    def test_create_product_failes(self, mock_save):
        product = Product()
        mock_save.side_effect = Exception('Test error')

        with self.assertRaises(ProductError):
            ProductDB.create_product(product)

    @mock.patch('business_logic.models.Product.objects.get')
    @mock.patch('business_logic.models.Product.save')
    def test_edit_field_prodcut_sub_true(self, mock_save, mock_get):
        id = 1
        mock_get.return_value = Product(id=id, stock=100, sku="sku1", name="Product1")
        mock_save.return_value = None

        result = ProductDB.edit_field_prodcut(id=id, stock=50, sub=True)

        self.assertTrue(result)

    @mock.patch('business_logic.models.Product.objects.get')
    @mock.patch('business_logic.models.Product.save')
    def test_edit_field_prodcut_sub_false(self, mock_save, mock_get):
        id = 1
        mock_get.return_value = Product(id=id, stock=100, sku="sku1", name="Product1")
        mock_save.return_value = None

        result = ProductDB.edit_field_prodcut(id=id, stock=50)

        self.assertTrue(result)

    @mock.patch('business_logic.models.Product.objects.get')
    @mock.patch('business_logic.models.Product.save')
    def test_edit_field_prodcut_error(self, mock_save, mock_get):
        id = 1
        mock_get.return_value = Product(id=id, stock=100, sku="sku1", name="Product1")
        mock_save.side_effect = Exception('Test error')

        # Act/Assert
        with self.assertRaises(ProductError):
            ProductDB.edit_field_prodcut(id=id, stock=50, sub=True)