import json
from django.contrib.messages import get_messages
from django.test import TestCase
from django.urls import reverse
from .models import *


class ProductTest(TestCase):
    fixtures = ['test_data.json']

    def add_order(self, product_id, qty, customer_id, customer_is_vip):
        data = {
            'product_id': Product.objects.get(product_id=product_id),
            'qty': qty,
            'customer_id': customer_id,
            'customer_is_vip': customer_is_vip,
        }
        return self.client.post(reverse('add_order'), data)

    def remove_order(self, order_id):
        data = {
            'order_id': order_id,
        }
        return self.client.post(reverse('remove_order'), data)

    def has_target_message_in_messages(self, response, target_message):
        messages = list(get_messages(response.wsgi_request))
        for message in messages:
            if str(message) == target_message:
                return True
        return False

    def test_add_order(self):
        self.assertEqual(Order.objects.all().count(), 2)
        self.add_order(
            product_id=2, qty=1, customer_id=5, customer_is_vip=False)
        self.assertEqual(Order.objects.all().count(), 3)

    def test_remove_order(self):
        self.assertEqual(Order.objects.all().count(), 2)
        self.remove_order(order_id=2)
        self.assertEqual(Order.objects.all().count(), 1)

    def test_add_product_but_not_enough_in_stock(self):
        product_id = 2
        qty = Product.objects.get(product_id=product_id).stock_pcs + 1
        response = self.add_order(product_id=product_id, qty=qty, customer_id=5,
                                  customer_is_vip=False)
        self.assertTrue(self.has_target_message_in_messages(
            response, 'Not enough product qty in stock!'))

    def test_add_vip_product_by_non_vip_customer(self):
        response = self.add_order(product_id=1, qty=1, customer_id=5,
                                  customer_is_vip=False)
        self.assertTrue(self.has_target_message_in_messages(
            response, 'Must be VIP'))

    def test_remove_order_hint_product_in_stock(self):
        self.add_order(product_id=3, qty=2, customer_id=5,
                       customer_is_vip=False)
        self.assertEqual(Order.objects.all().count(), 3)
        response = self.remove_order(order_id=3)
        self.assertTrue(self.has_target_message_in_messages(
            response, 'Product 3 in stock now!'))

    def test_top_3(self):
        response = self.client.get(reverse('get_top_3_products'))
        data = response.content.decode('utf-8')

        answer = json.loads(
            '{"1": {"product_id": 1, "total": 2}, "2": {"product_id": 3, "total": 1}}')
        self.assertEqual(answer, json.loads(data))

        self.add_order(product_id=2, qty=3, customer_id=5,
                       customer_is_vip=False)
        response = self.client.get(reverse('get_top_3_products'))
        data = response.content.decode('utf-8')

        answer = json.loads(
            '{"1": {"product_id": 2, "total": 3}, "2": {"product_id": 1, "total": 2}, "3": {"product_id": 3, "total": 1}}')
        self.assertEqual(answer, json.loads(data))
