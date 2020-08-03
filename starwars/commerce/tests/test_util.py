import uuid
from rest_framework.test import APITestCase
from commerce import models


def create_fake_advertiser():
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


def create_fake_order(advertiser_id=None):
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
        advertiser = test_util.create_fake_advertiser()
        order.advertiser = advertiser

    order.save()
    return order
