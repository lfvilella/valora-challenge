from rest_framework.generics import ListAPIView

from . import models, serializers


class OrderApi(ListAPIView):
    queryset = models.Order.objects.all()
    serializer_class = serializers.OrderSerializer


class ToolApi(ListAPIView):
    queryset = models.Tool.objects.all()
    serializer_class = serializers.ToolSerializer
