from rest_framework.test import APITestCase
from commerce import models

from . import test_util


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

        response = self.client.post("/advertiser/", self.data, format="json")

        self.assertEqual(models.Advertiser.objects.count(), 1)

        advertiser = models.Advertiser.objects.all().first()

        expected_value = {
            "user": {
                "id": advertiser.user.pk,
                "username": advertiser.user.username,
                "email": advertiser.user.email
            },
            "phone": advertiser.phone,
        }
        self.assertEqual(response.json(), expected_value)

    def test_allow_login_after_creation(self):
        self.client.post("/advertiser/", self.data, format="json")

        login_data = {
            'username': self.data['user']['username'],
            'password': self.data['user']['password'],
        }
        login_response = self.client.post(
            "/user-auth/", login_data, format="json"
        )
        self.assertEqual(login_response.status_code, 200)


class TestReadAdvertiser(TestAdvertiserBase):
    def test_get_details_logged_user(self):
        advertiser = test_util.create_fake_advertiser()
        self.client.login(
            username=advertiser.user.username,
            password=advertiser.user.test_password,
        )

        response = self.client.get("/advertiser/", {}, format="json")

        expected_value = {
            "user": {
                "id": advertiser.user.pk,
                "username": advertiser.user.username,
                "email": advertiser.user.email,
            },
            "phone": advertiser.phone,
        }
        self.assertEqual(response.json(), expected_value)

    def test_when_user_is_not_logged_redirect_to_login(self):
        test_util.create_fake_advertiser()
        response = self.client.get("/advertiser/", {}, format="json")
        self.assertEqual(response.status_code, 302)
