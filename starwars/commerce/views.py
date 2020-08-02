from django.shortcuts import get_object_or_404

from rest_framework import views
from rest_framework import response
from rest_framework import status

from . import models, serializers, services


class OrderAPIView(views.APIView):

    serializer_class = serializers.OrderSerializer

    def _detail(self, request, order_id):
        order = get_object_or_404(models.Order, pk=order_id)
        serializer = serializers.OrderSerializer(order)
        return response.Response(serializer.data, status=status.HTTP_200_OK)

    def _list(self, request):
        return response.Response([], status=status.HTTP_200_OK)

    def get(self, request, order_id=None):
        if order_id:
            return self._detail(request, order_id)
        return self._list(request)

    def post(self, request):
        serializer = serializers.OrderSerializer(data=request.data)
        if not serializer.is_valid():
            return response.Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )

        serializer.save()
        return response.Response(
            serializer.data, status=status.HTTP_201_CREATED
        )

    def put(self, request, order_id):
        order = get_object_or_404(models.Order, pk=order_id)

        serializer = serializers.OrderSerializer(
            instance=order, data=request.data
        )
        if not serializer.is_valid():
            return response.Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )

        serializer.save()
        return response.Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, order_id):
        order = get_object_or_404(models.Order, pk=order_id)
        services.delete_order(order.pk)

        return response.Response({}, status=status.HTTP_204_NO_CONTENT)

    def patch(self, request, order_id):
        order = get_object_or_404(models.Order, pk=order_id)

        serializer = serializers.OrderPatchSerializer(
            instance=order, data=request.data
        )
        if not serializer.is_valid():
            return response.Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )

        serializer.save()
        return response.Response(serializer.data, status=status.HTTP_200_OK)
