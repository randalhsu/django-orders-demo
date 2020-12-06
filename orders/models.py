from django.db import models


class Shop(models.Model):
    shop_id = models.TextField(primary_key=True)

    def __str__(self):
        return f'{self.shop_id}'


class Customer(models.Model):
    customer_id = models.AutoField('Customer ID', primary_key=True)

    def __str__(self):
        return f'{self.customer_id}'


class Product(models.Model):
    product_id = models.AutoField('Product ID', primary_key=True)
    stock_pcs = models.IntegerField('Stock PCS')
    price = models.IntegerField('Price')
    shop_id = models.ForeignKey(Shop, on_delete=models.PROTECT)
    vip = models.BooleanField()

    def __str__(self):
        return f'{self.product_id}'


class Order(models.Model):
    order_id = models.AutoField('Order ID', primary_key=True)
    product_id = models.ForeignKey(Product, on_delete=models.PROTECT)
    qty = models.IntegerField('Quantity')
    price = models.IntegerField('Price')
    shop_id = models.ForeignKey(Shop, on_delete=models.PROTECT)
    customer_id = models.ForeignKey(Customer, on_delete=models.PROTECT)

    def __str__(self):
        return f'{self.order_id}'
