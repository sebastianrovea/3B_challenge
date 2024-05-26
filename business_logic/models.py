from django.utils import timezone

from django.db import models


class Product(models.Model):
    sku = models.CharField(unique=True, max_length=55)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    stock = models.IntegerField(null=False, default=100)

    def __str__(self) -> str:
        return str(self.id)


class Order(models.Model):
    client = models.CharField(max_length=55)
    date_order = models.DateTimeField(default=timezone.now)

    def __str__(self) -> str:
        return str(self.id)


class OrderLine(models.Model):
    order_id = models.IntegerField()
    product_id = models.IntegerField()

    def __str__(self) -> str:
        return str(self.id)