from rest_framework import serializers
from . import models


class OrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Order
        fields = ['id', 'item', 'status']


class AdvertiserSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Advertiser


class ToolSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Tool
        fields = ['id', 'name', 'description']
