from rest_framework import serializers
from . import models
from . import services


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Item
        fields = ["name", "description"]


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ["username", "password", "email"]


class AdvertiserSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=True)

    class Meta:
        model = models.Advertiser
        fields = ["user", "phone"]

    def create(self, validated_data):
        return services.create_advertiser(validated_data)


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Address
        fields = [
            "state",
            "address",
            "neighborhood",
            "number",
            "complement",
            "city",
            "cep",
        ]


class OrderPatchSerializer(serializers.ModelSerializer):
    item = ItemSerializer(required=False)
    shipping_address = AddressSerializer(required=False)

    class Meta:
        model = models.Order
        fields = ["item", "shipping_address", "status"]

    def update(self, instance, validated_data):
        return services.update_order(instance.pk, validated_data)


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
