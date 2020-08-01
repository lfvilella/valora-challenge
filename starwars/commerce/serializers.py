from rest_framework import serializers
from . import models
from . import services


class AdvertiserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Advertiser
        fields = ["user", "phone"]


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Item
        fields = ["id", "name", "description"]


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ["username", "email", "password"]


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
