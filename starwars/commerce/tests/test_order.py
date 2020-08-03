import uuid
from rest_framework.test import APITestCase
from commerce import models

from . import test_util


class TestOrderBase(APITestCase):
    def setUp(self):
        self.data = {
            "item": {"name": "engine", "description": "engine c3po"},
            "shipping_address": {
                "state": "SP",
                "address": "Fake Address",
                "neighborhood": "Fake Neighborhood",
                "number": "111",
                "complement": "Fake Complement",
                "city": "Fake City",
                "cep": "Fake Cep",
            },
        }

    def _create_and_log_in_user(self):
        advertiser = test_util.create_fake_advertiser()
        self.client.login(
            username=advertiser.user.username,
            password=advertiser.user.test_password,
        )
        return advertiser


class TestCreateOrder(TestOrderBase):
    def test_returns_201(self):
        self._create_and_log_in_user()

        response = self.client.post("/order/", self.data, format="json")
        self.assertEqual(response.status_code, 201)

    def test_saves_on_db(self):
        self._create_and_log_in_user()

        self.assertEqual(models.Order.objects.count(), 0)

        self.client.post("/order/", self.data, format="json")

        self.assertEqual(models.Order.objects.count(), 1)

        order = models.Order.objects.all().first()

        expected_value = {
            "item": {
                "name": order.item.name,
                "description": order.item.description,
            },
            "shipping_address": {
                "state": order.shipping_address.state,
                "address": order.shipping_address.address,
                "neighborhood": order.shipping_address.neighborhood,
                "number": order.shipping_address.number,
                "complement": order.shipping_address.complement,
                "city": order.shipping_address.city,
                "cep": order.shipping_address.cep,
            },
        }
        self.assertEqual(self.data, expected_value)

    def test_create_order_default_status_is_open(self):
        self._create_and_log_in_user()

        self.client.post("/order/", self.data, format="json")

        order = models.Order.objects.all().first()
        self.assertEqual(order.status, "open")

    def test_check_logged_user_is_advertiser(self):
        advertiser = self._create_and_log_in_user()

        self.client.post("/order/", self.data, format="json")

        order = models.Order.objects.all().first()
        self.assertEqual(order.advertiser, advertiser)


class TestUpdateOrder(TestOrderBase):
    def test_update_order(self):
        advertiser = self._create_and_log_in_user()
        order = test_util.create_fake_order(advertiser_id=advertiser.pk)

        response = self.client.put(
            f"/order/{order.pk}", self.data, format="json"
        )
        self.assertEqual(response.status_code, 200)

        order.refresh_from_db()
        self.assertEqual(order.item.name, "engine")

    def test_update_order_with_invalid_user(self):
        advertiser = test_util.create_fake_advertiser()
        order = test_util.create_fake_order(advertiser_id=advertiser.pk)

        logged_advertiser = self._create_and_log_in_user()

        self.assertNotEqual(advertiser.pk, logged_advertiser.pk)

        response = self.client.put(
            f"/order/{order.pk}", self.data, format="json"
        )
        self.assertEqual(response.status_code, 404)

    def test_finalize_order(self):
        advertiser = self._create_and_log_in_user()
        order = test_util.create_fake_order(advertiser_id=advertiser.pk)

        self.assertEqual(order.status, "open")

        data = {"status": "finished"}
        response = self.client.patch(f"/order/{order.pk}", data, format="json")
        self.assertEqual(response.status_code, 200)

        order.refresh_from_db()
        self.assertEqual(order.status, "finished")


class TestReadOrder(TestOrderBase):
    def test_get_order(self):
        advertiser = self._create_and_log_in_user()
        order = test_util.create_fake_order(advertiser_id=advertiser.pk)

        response = self.client.get(f"/order/{order.pk}", {}, format="json")
        self.assertEqual(response.status_code, 200)

        expected_value = {
            "id": order.pk,
            "item": {
                "name": order.item.name,
                "description": order.item.description,
            },
            "shipping_address": {
                "state": order.shipping_address.state,
                "address": order.shipping_address.address,
                "neighborhood": order.shipping_address.neighborhood,
                "number": order.shipping_address.number,
                "complement": order.shipping_address.complement,
                "city": order.shipping_address.city,
                "cep": order.shipping_address.cep,
            },
            "status": order.status,
        }
        self.assertEqual(response.json(), expected_value)

    def test_get_order_with_invalid_user(self):
        advertiser = self._create_and_log_in_user()
        order = test_util.create_fake_order(advertiser_id=advertiser.pk)

        self._create_and_log_in_user()  # new user logged
        response = self.client.get(f"/order/{order.pk}", {}, format="json")
        self.assertEqual(response.status_code, 404)

    def test_list_order(self):
        advertiser = self._create_and_log_in_user()
        # Create two orders
        order1 = test_util.create_fake_order(advertiser_id=advertiser.pk)
        order2 = test_util.create_fake_order(advertiser_id=advertiser.pk)

        response = self.client.get("/order/", {}, format="json")
        self.assertEqual(response.status_code, 200)

        expected_value = [
            {
                "id": order1.pk,
                "item": {
                    "name": order1.item.name,
                    "description": order1.item.description,
                },
                "shipping_address": {
                    "state": order1.shipping_address.state,
                    "address": order1.shipping_address.address,
                    "neighborhood": order1.shipping_address.neighborhood,
                    "number": order1.shipping_address.number,
                    "complement": order1.shipping_address.complement,
                    "city": order1.shipping_address.city,
                    "cep": order1.shipping_address.cep,
                },
                "status": order1.status,
            },
            {
                "id": order2.pk,
                "item": {
                    "name": order2.item.name,
                    "description": order2.item.description,
                },
                "shipping_address": {
                    "state": order2.shipping_address.state,
                    "address": order2.shipping_address.address,
                    "neighborhood": order2.shipping_address.neighborhood,
                    "number": order2.shipping_address.number,
                    "complement": order2.shipping_address.complement,
                    "city": order2.shipping_address.city,
                    "cep": order2.shipping_address.cep,
                },
                "status": order2.status,
            },
        ]
        self.assertEqual(response.json(), expected_value)

    def test_list_order_is_empity(self):
        self._create_and_log_in_user()
        response = self.client.get("/order/", {}, format="json")
        self.assertEqual(response.json(), [])


class TestDeleteOrder(TestOrderBase):
    def test_delete_order(self):
        advertiser = self._create_and_log_in_user()
        order = test_util.create_fake_order(advertiser_id=advertiser.pk)

        self.assertEqual(models.Order.objects.count(), 1)

        response = self.client.delete(f"/order/{order.pk}", {}, format="json")
        self.assertEqual(response.status_code, 200)

        self.assertEqual(models.Order.objects.count(), 0)

    def test_delete_order_with_invalid_user(self):
        advertiser = self._create_and_log_in_user()
        order = test_util.create_fake_order(advertiser_id=advertiser.pk)

        self._create_and_log_in_user()  # new user logged
        response = self.client.delete(f"/order/{order.pk}", {}, format="json")
        self.assertEqual(response.status_code, 404)
