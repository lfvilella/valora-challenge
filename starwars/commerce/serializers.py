from django.contrib import auth

from rest_framework import serializers

from . import models
from . import services


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Item
        fields = ["name", "description"]


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    def validate(self, data):
        username = data["username"]
        password = data["password"]
        user = auth.authenticate(username=username, password=password)
        if not user:
            raise serializers.ValidationError("Invalid Credentials")
        return data


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ["id", "username", "email"]


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ["username", "password", "email"]


class AdvertiserGetSerializer(serializers.ModelSerializer):
    user = UserDetailSerializer(required=True)

    class Meta:
        model = models.Advertiser
        fields = ["user", "phone"]


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


class OrderSerializer(serializers.ModelSerializer):
    item = ItemSerializer(required=True)
    shipping_address = AddressSerializer(required=True)

    class Meta:
        model = models.Order
        fields = ["item", "shipping_address", "status"]
