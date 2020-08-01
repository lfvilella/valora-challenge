from rest_framework import serializers
from . import models
from . import services


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Item
        fields = ["id", "name", "description"]


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Address
        fields = ["state"]


class OrderSerializer(serializers.ModelSerializer):
    item = ItemSerializer(required=True)
    shipping_address = AddressSerializer(required=True)

    class Meta:
        model = models.Order
        fields = ["item", "shipping_address", "status"]

    def create(self, validated_data):
        return services.create_order(validated_data)

    def update(self, instance, validated_data):
        return services.update_order(instance.pk, validated_data)
