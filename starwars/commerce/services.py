from . import models


def create_order(validated_data):
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
    )
    shipping_address.save()

    order.shipping_address = shipping_address
    order.save()
    return order


def update_order(order_id, validated_data):
    order = models.Order.objects.get(pk=order_id)
    order.status = validated_data.get("status", order.status)
    order.item.name = validated_data["item"]["name"]
    order.item.description = validated_data["item"]["description"]
    order.shipping_address.state = validated_data["shipping_address"].get(
        "state"
    )
    order.save()
    return order
