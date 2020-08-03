from django.contrib import auth

from . import models


def get_order(order_id, user_id):
    order = None
    try:
        order = models.Order.objects.get(pk=order_id)
    except models.Order.DoesNotExist:
        return None

    advertiser = get_advertiser_by_user_id(user_id)
    if not advertiser:
        return None

    if order.advertiser.id != advertiser.user.pk:
        return None

    return order


def list_order(user_id):
    orders = models.Order.objects.filter(advertiser__user__pk=user_id).all()
    if not orders:
        return []

    return orders


def create_order(validated_data, user_id):
    order = models.Order()
    order.status = models.Order.STATUS_OPEN

    item = models.Item(
        name=validated_data["item"]["name"],
        description=validated_data["item"]["description"],
    )
    item.save()
    order.item = item

    shipping_address = models.Address(
        state=validated_data["shipping_address"].get("state"),
        address=validated_data["shipping_address"].get("address"),
        neighborhood=validated_data["shipping_address"].get("neighborhood"),
        number=validated_data["shipping_address"].get("number"),
        complement=validated_data["shipping_address"].get("complement"),
        city=validated_data["shipping_address"].get("city"),
        cep=validated_data["shipping_address"].get("cep"),
    )
    shipping_address.save()
    order.shipping_address = shipping_address

    advertiser = models.Advertiser.objects.get(pk=user_id)
    order.advertiser = advertiser

    order.save()
    return order


def update_order(order_id, validated_data, user_id):
    order = get_order(order_id, user_id)
    order.status = validated_data.get("status", order.status)
    if validated_data.get("item"):
        order.item.name = validated_data["item"].get("name", order.item.name)
        order.item.description = validated_data["item"].get(
            "description", order.item.description
        )
        order.item.save()

    if validated_data.get("shipping_address"):
        order.shipping_address.state = validated_data["shipping_address"].get(
            "state", order.shipping_address.state
        )
        order.shipping_address.save()

    if not order.advertiser:
        advertiser = models.Advertiser.objects.get(pk=user_id)
        order.advertiser = advertiser

    order.save()
    return order


def delete_order(order_id, user_id):
    order = get_order(order_id, user_id)
    if not order:
        return None

    order.delete()
    return order


# Advertiser


def create_advertiser(validated_data):
    advertiser = models.Advertiser()
    advertiser.phone = validated_data["phone"]

    user = models.User(
        username=validated_data["user"]["username"],
        password=validated_data["user"]["password"],
        email=validated_data["user"].get("email"),
    )
    user.save()

    advertiser.user = user
    advertiser.save()
    return advertiser


def get_advertiser_by_user_id(user_id):
    try:
        return models.Advertiser.objects.get(user__id=user_id)
    except models.Advertiser.DoesNotExist:
        return None


def user_login(request, username, password):
    user = auth.authenticate(request, username=username, password=password)
    if not user:
        return None

    auth.login(request, user)
    return user


def user_logout(request):
    return auth.logout(request)
