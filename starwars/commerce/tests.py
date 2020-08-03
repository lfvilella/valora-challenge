import uuid
from rest_framework.test import APITestCase
from . import models


def _create_fake_advertiser():
    advertiser = models.Advertiser()
    advertiser.phone = "Fake Phone"

    password = "FakePassword"
    user = models.User.objects.create_user(
        username=str(uuid.uuid4()), password=password, email="fake@email.com",
    )
    user.test_password = password
    user.save()

    advertiser.user = user
    advertiser.save()
    return advertiser


class TestLogin(APITestCase):
    def setUp(self):
        self.advertiser = _create_fake_advertiser()
        self.data = {
            "username": self.advertiser.user.username,
            "password": self.advertiser.user.test_password
        }

    def test_valid_login_returns_200(self):
        response = self.client.post("/user-auth/", self.data, format="json")
        self.assertEqual(response.status_code, 200)

    def test_valid_login_returns_user_info(self):
        response = self.client.post("/user-auth/", self.data, format="json")
        expected_value = {
            "id": self.advertiser.user.pk,
            "username": self.advertiser.user.username,
            "email": self.advertiser.user.email
        }
        self.assertEqual(response.json(), expected_value)

    def test_invalid_login_returns_400(self):
        self.data['password'] = "Wrong Password"
        response = self.client.post("/user-auth/", self.data, format="json")
        self.assertEqual(response.status_code, 400)


class TestLogout(APITestCase):
    def test_returns_204(self):
        advertiser = _create_fake_advertiser()
        self.client.login(
            username=advertiser.user.username,
            password=advertiser.user.test_password,
        )
        response = self.client.delete("/user-auth/", {}, format="json")
        self.assertEqual(response.status_code, 204)

    def test_deny_access(self):
        advertiser = _create_fake_advertiser()
        self.client.login(
            username=advertiser.user.username,
            password=advertiser.user.test_password,
        )
        response = self.client.get("/advertiser/", {}, format="json")
        self.assertEqual(response.status_code, 200)

        self.client.delete("/user-auth/", {}, format="json")
        response = self.client.get("/advertiser/", {}, format="json")
        self.assertEqual(response.status_code, 302)



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

    def _create_fake_order(self, advertiser_id=None):
        order = models.Order()
        order.status = models.Order.STATUS_OPEN

        # Create Item
        item = models.Item(name="xyz", description="xyz")
        item.save()
        order.item = item

        # Create Shipping_Address
        shipping_address = models.Address(
            address="Fake Address",
            neighborhood="Fake Neighborhood",
            number="111",
            complement="Fake Complement",
            city="Fake City",
            cep="Fake CEP",
        )
        shipping_address.save()
        order.shipping_address = shipping_address

        if advertiser_id:
            order.advertiser_id = advertiser_id
        else:
            advertiser = _create_fake_advertiser()
            order.advertiser = advertiser

        order.save()
        return order

    def _create_and_log_in_user(self):
        advertiser = _create_fake_advertiser()
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
        order = self._create_fake_order(advertiser_id=advertiser.pk)

        response = self.client.put(
            f"/order/{order.pk}", self.data, format="json"
        )
        self.assertEqual(response.status_code, 200)

        order.refresh_from_db()
        self.assertEqual(order.item.name, "engine")

    def test_update_order_with_invalid_user(self):
        advertiser = _create_fake_advertiser()
        order = self._create_fake_order(advertiser_id=advertiser.pk)

        logged_advertiser = self._create_and_log_in_user()

        self.assertNotEqual(advertiser.pk, logged_advertiser.pk)

        response = self.client.put(
            f"/order/{order.pk}", self.data, format="json"
        )
        self.assertEqual(response.status_code, 404)

    def test_finalize_order(self):
        advertiser = self._create_and_log_in_user()
        order = self._create_fake_order(advertiser_id=advertiser.pk)

        self.assertEqual(order.status, "open")

        data = {"status": "finished"}
        response = self.client.patch(f"/order/{order.pk}", data, format="json")
        self.assertEqual(response.status_code, 200)

        order.refresh_from_db()
        self.assertEqual(order.status, "finished")


class TestReadOrder(TestOrderBase):
    def test_get_order(self):
        advertiser = self._create_and_log_in_user()
        order = self._create_fake_order(advertiser_id=advertiser.pk)

        response = self.client.get(f"/order/{order.pk}", {}, format="json")
        self.assertEqual(response.status_code, 200)

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
            "status": order.status,
        }
        self.assertEqual(response.json(), expected_value)

    def test_get_order_with_invalid_user(self):
        advertiser = self._create_and_log_in_user()
        order = self._create_fake_order(advertiser_id=advertiser.pk)

        self._create_and_log_in_user()  # new user logged
        response = self.client.get(f"/order/{order.pk}", {}, format="json")
        self.assertEqual(response.status_code, 404)

    def test_list_order(self):
        advertiser = self._create_and_log_in_user()
        # Create two orders
        order1 = self._create_fake_order(advertiser_id=advertiser.pk)
        order2 = self._create_fake_order(advertiser_id=advertiser.pk)

        response = self.client.get("/order/", {}, format="json")
        self.assertEqual(response.status_code, 200)

        expected_value = [
            {
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
        order = self._create_fake_order(advertiser_id=advertiser.pk)

        self.assertEqual(models.Order.objects.count(), 1)

        response = self.client.delete(f"/order/{order.pk}", {}, format="json")
        self.assertEqual(response.status_code, 204)

        self.assertEqual(models.Order.objects.count(), 0)

    def test_delete_order_with_invalid_user(self):
        advertiser = self._create_and_log_in_user()
        order = self._create_fake_order(advertiser_id=advertiser.pk)

        self._create_and_log_in_user()  # new user logged
        response = self.client.delete(f"/order/{order.pk}", {}, format="json")
        self.assertEqual(response.status_code, 404)


# Test Advertiser


class TestAdvertiserBase(APITestCase):
    def setUp(self):
        self.data = {
            "user": {
                "username": "FakeUsername",
                "password": "FakePassword",
                "email": "fake@email.com",
            },
            "phone": "Fake Phone",
        }


class TestCreateAdvertiser(TestAdvertiserBase):
    def test_returns_201(self):
        response = self.client.post("/advertiser/", self.data, format="json")
        self.assertEqual(response.status_code, 201)

    def test_saves_on_db(self):
        self.assertEqual(models.Advertiser.objects.count(), 0)

        self.client.post("/advertiser/", self.data, format="json")

        self.assertEqual(models.Advertiser.objects.count(), 1)

        advertiser = models.Advertiser.objects.all().first()

        expected_value = {
            "user": {
                "username": advertiser.user.username,
                "password": advertiser.user.password,
                "email": advertiser.user.email,
            },
            "phone": advertiser.phone,
        }
        self.assertEqual(self.data, expected_value)


class TestReadAdvertiser(TestAdvertiserBase):
    def test_get_details_logged_user(self):
        advertiser = _create_fake_advertiser()
        self.client.login(
            username=advertiser.user.username,
            password=advertiser.user.test_password,
        )

        response = self.client.get("/advertiser/", {}, format="json")

        expected_value = {
            "user": {
                "id": advertiser.user.pk,
                "username": advertiser.user.username,
                "email": advertiser.user.email
            },
            "phone": advertiser.phone,
        }
        self.assertEqual(response.json(), expected_value)

    def test_when_user_is_not_logged_redirect_to_login(self):
        _create_fake_advertiser()
        response = self.client.get("/advertiser/", {}, format="json")
        self.assertEqual(response.status_code, 302)
