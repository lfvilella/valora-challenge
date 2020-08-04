""" Services

This module is responsible to handle all interactions to the database
and bussiness rules.
"""

import typing

from django.contrib import auth

from . import models


def get_order(order_id: int, user_id: int) -> models.Order:
    """ Get Order.

    Args:
        order_id: Order ID.
        user_id: User ID.

    Returns:
        A models.Order.
    """

    order = None
    try:
        order = models.Order.objects.get(pk=order_id)
    except models.Order.DoesNotExist:
        return None

    advertiser = get_advertiser_by_user_id(user_id)
    if not advertiser:
        return None

    if advertiser.user.is_superuser:
        return order

    if order.advertiser.user.id != advertiser.user.pk:
        return None

    return order


def list_orders(user_id: int) -> typing.List[models.Order]:
    """ List Orders.

    Args:
        user_id: User ID.

    Returns:
        Filtered orders if user is not superuser.
        All orders if user is superuser.
    """

    advertiser = get_advertiser_by_user_id(user_id)

    orders = models.Order.objects.filter(
        advertiser__user__pk=advertiser.user.pk
    ).all()

    if advertiser.user.is_superuser:
        return models.Order.objects.all()

    if not orders:
        return []

    return orders


def create_order(validated_data: dict, user_id: int) -> models.Order:
    """ Create Order.

    Args:
        validated_data: Dictionary containing order information.
        user_id: User ID.

    Returns:
        A models.Order.
    """

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

    advertiser = get_advertiser_by_user_id(user_id)
    order.advertiser = advertiser

    order.save()
    return order


def update_order(
    order_id: int, validated_data: dict, user_id: int
) -> models.Order:
    """ Update Order.

    Args:
        order_id: Order ID.
        validated_data: Dictionary containing order information.
        user_id: User ID.

    Returns:
        A models.Order.
    """

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


def delete_order(order_id: int, user_id: int) -> models.Order:
    """ Delete Order.

    Args:
        order_id: Order ID.
        user_id: User ID.

    Returns:
        A models.Order.
    """

    order = get_order(order_id, user_id)
    if not order:
        return None

    order.delete()
    return order


# Advertiser


def create_advertiser(validated_data: dict) -> models.Advertiser:
    """ Create Advertiser.

    Args:
        validated_data: Dictionary containing advertiser information.

    Returns:
        A models.Advertiser.
    """

    advertiser = models.Advertiser()
    advertiser.phone = validated_data["phone"]

    user = models.User.objects.create_user(
        username=validated_data["user"]["username"],
        password=validated_data["user"]["password"],
        email=validated_data["user"].get("email"),
    )

    advertiser.user = user
    advertiser.save()
    return advertiser


def get_advertiser_by_user_id(user_id: int) -> models.Advertiser:
    """ Get Advertiser By User Id.

    Args:
        user_id: User ID.

    Returns:
        A models.Advertiser.
    """

    try:
        return models.Advertiser.objects.get(user__id=user_id)
    except models.Advertiser.DoesNotExist:
        return None


def user_login(request, username: str, password: str) -> models.User:
    """ User Login.

    Args:
        request: A request.
        username: A username.
        password: A password.

    Returns:
        A models.User.
    """

    user = auth.authenticate(request, username=username, password=password)
    if not user:
        return None

    auth.login(request, user)
    return user


def user_logout(request):
    return auth.logout(request)
