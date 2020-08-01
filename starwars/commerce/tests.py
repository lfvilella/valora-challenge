from rest_framework.test import APITestCase
from . import models


class TestOrderAPI(APITestCase):
    def test_create_order(self):
        data = {
            "item": {"name": "engine", "description": "engine c3po"},
            "shipping_address": {"state": "SP"},
        }

        self.assertEqual(models.Order.objects.count(), 0)

        response = self.client.post("/order/", data, format="json")
        self.assertEqual(response.status_code, 201)

        self.assertEqual(models.Order.objects.count(), 1)

    def test_update_order(self):
        order = models.Order()
        order.status = models.Order.STATUS_OPEN

        item = models.Item(name="xyz", description="xyz")
        item.save()
        order.item = item

        shipping_address = models.Address(state="SP")
        shipping_address.save()

        order.shipping_address = shipping_address
        order.save()

        data = {
            "item": {"name": "engine", "description": "engine c3po"},
            "shipping_address": {"state": "SP"},
        }

        response = self.client.put(f"/order/{order.pk}", data, format="json")
        self.assertEqual(response.status_code, 200)
