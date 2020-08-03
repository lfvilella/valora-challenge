import uuid
from rest_framework.test import APITestCase
from commerce import models

from . import test_util


class TestAdministrador(APITestCase):
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

    def _create_fake_admin(self):
        advertiser = models.Advertiser()
        advertiser.phone = "Admin Fake Phone"

        password = "AdminFakePassword"
        user = models.User.objects.create_user(
            username=str(uuid.uuid4()),
            password=password,
            email="fake@email.com",
            is_superuser=True,
        )
        user.test_password = password
        user.save()

        advertiser.user = user
        advertiser.save()
        return advertiser

    def test_create_superuser(self):
        adm = self._create_fake_admin()
        self.assertEqual(adm.user.is_superuser, True)

    def test_get_order(self):
        advertiser = test_util.create_fake_advertiser()
        order = test_util.create_fake_order(advertiser_id=advertiser.pk)

        adm = self._create_fake_admin()
        self.client.login(
            username=adm.user.username, password=adm.user.test_password,
        )

        response = self.client.get(f"/order/{order.pk}", {}, format="json")
        self.assertEqual(response.status_code, 200)

    def test_list_order(self):
        advertiser1 = test_util.create_fake_advertiser()
        order1 = test_util.create_fake_order(advertiser_id=advertiser1.pk)

        advertiser2 = test_util.create_fake_advertiser()
        order2 = test_util.create_fake_order(advertiser_id=advertiser2.pk)

        adm = self._create_fake_admin()
        self.client.login(
            username=adm.user.username, password=adm.user.test_password,
        )
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

    def test_delete_order(self):
        advertiser = test_util.create_fake_advertiser()
        order = test_util.create_fake_order(advertiser_id=advertiser.pk)

        self.assertEqual(models.Order.objects.count(), 1)

        self._create_and_log_in_user()  # new user logged
        response = self.client.delete(f"/order/{order.pk}", {}, format="json")
        self.assertEqual(response.status_code, 404)

        adm = self._create_fake_admin()
        self.client.login(
            username=adm.user.username, password=adm.user.test_password,
        )
        response = self.client.delete(f"/order/{order.pk}", {}, format="json")
        self.assertEqual(response.status_code, 200)

        self.assertEqual(models.Order.objects.count(), 0)

    def test_update_order(self):
        advertiser = test_util.create_fake_advertiser()
        order = test_util.create_fake_order(advertiser_id=advertiser.pk)

        adm = self._create_fake_admin()
        self.client.login(
            username=adm.user.username, password=adm.user.test_password,
        )

        self.assertNotEqual(advertiser.pk, adm.pk)

        response = self.client.put(
            f"/order/{order.pk}", self.data, format="json"
        )
        self.assertEqual(response.status_code, 200)

    def test_finalize_order(self):
        advertiser = self._create_and_log_in_user()
        order = test_util.create_fake_order(advertiser_id=advertiser.pk)

        self.assertEqual(order.status, "open")

        adm = self._create_fake_admin()
        self.client.login(
            username=adm.user.username, password=adm.user.test_password,
        )
        data = {"status": "finished"}
        response = self.client.patch(f"/order/{order.pk}", data, format="json")
        self.assertEqual(response.status_code, 200)

        order.refresh_from_db()
        self.assertEqual(order.status, "finished")
