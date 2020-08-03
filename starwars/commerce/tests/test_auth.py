import uuid
from rest_framework.test import APITestCase
from commerce import models

from . import test_util


class TestLogin(APITestCase):
    def setUp(self):
        self.advertiser = test_util.create_fake_advertiser()
        self.data = {
            "username": self.advertiser.user.username,
            "password": self.advertiser.user.test_password,
        }

    def test_valid_login_returns_200(self):
        response = self.client.post("/user-auth/", self.data, format="json")
        self.assertEqual(response.status_code, 200)

    def test_valid_login_returns_user_info(self):
        response = self.client.post("/user-auth/", self.data, format="json")
        expected_value = {
            "id": self.advertiser.user.pk,
            "username": self.advertiser.user.username,
            "email": self.advertiser.user.email,
        }
        self.assertEqual(response.json(), expected_value)

    def test_invalid_login_returns_400(self):
        self.data["password"] = "Wrong Password"
        response = self.client.post("/user-auth/", self.data, format="json")
        self.assertEqual(response.status_code, 400)


class TestLogout(APITestCase):
    def test_returns_204(self):
        advertiser = test_util.create_fake_advertiser()
        self.client.login(
            username=advertiser.user.username,
            password=advertiser.user.test_password,
        )
        response = self.client.delete("/user-auth/", {}, format="json")
        self.assertEqual(response.status_code, 204)

    def test_deny_access(self):
        advertiser = test_util.create_fake_advertiser()
        self.client.login(
            username=advertiser.user.username,
            password=advertiser.user.test_password,
        )
        response = self.client.get("/advertiser/", {}, format="json")
        self.assertEqual(response.status_code, 200)

        self.client.delete("/user-auth/", {}, format="json")
        response = self.client.get("/advertiser/", {}, format="json")
        self.assertEqual(response.status_code, 302)
