from rest_framework import decorators
from rest_framework import response
from rest_framework import status

from . import models, serializers


@decorators.api_view(["POST"])
def create_order(request):
    serializer = serializers.OrderSerializer(data=request.data)
    if not serializer.is_valid():
        return response.Response(
            serializer.errors, status=status.HTTP_400_BAD_REQUEST
        )

    serializer.save()
    return response.Response(serializer.data, status=status.HTTP_201_CREATED)


@decorators.api_view(["PUT"])
def update_order(request, order_id):
    order = None
    try:
        order = models.Order.objects.get(pk=order_id)
    except models.Order.DoesNotExist:
        return response.Response({}, status=status.HTTP_404_NOT_FOUND)

    serializer = serializers.OrderSerializer(instance=order, data=request.data)
    if not serializer.is_valid():
        return response.Response(
            serializer.errors, status=status.HTTP_400_BAD_REQUEST
        )

    serializer.save()
    return response.Response(serializer.data, status=status.HTTP_200_OK)
