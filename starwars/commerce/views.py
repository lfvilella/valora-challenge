from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.contrib.auth import decorators

from rest_framework import views
from rest_framework import response
from rest_framework import status
from rest_framework import permissions

from . import models, serializers, services


class OrderAPIView(views.APIView):

    permission_classes = [permissions.IsAuthenticated]

    def _check_users(self, advertiser_id, user_id):
        if advertiser_id != user_id:
            return response.Response({}, status=status.HTTP_403_FORBIDDEN)

    def _detail(self, request, order_id):
        order = get_object_or_404(models.Order, pk=order_id)
        # Needs to check why it doesn't work using self._check_users(...) !!!!
        if order.advertiser.id != request.user.pk:
            return response.Response({}, status=status.HTTP_403_FORBIDDEN)

        serializer = serializers.OrderSerializer(order)
        return response.Response(serializer.data, status=status.HTTP_200_OK)

    def _list(self, request):
        orders = models.Order.objects.filter(advertiser_id=request.user.pk)
        serializer_orders = []
        for order in orders:
            serializer = serializers.OrderSerializer(order)
            serializer_orders.append(serializer.data)

        return response.Response(serializer_orders, status=status.HTTP_200_OK)

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

        services.create_order(
            validated_data=serializer.validated_data, user_id=request.user.pk
        )

        serializer.save()
        return response.Response(
            serializer.data, status=status.HTTP_201_CREATED
        )

    def put(self, request, order_id):
        order = get_object_or_404(models.Order, pk=order_id)
        self._check_users(order.advertiser.id, request.user.pk)

        serializer = serializers.OrderSerializer(
            instance=order, data=request.data
        )
        if not serializer.is_valid():
            return response.Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )

        services.update_order(
            order_id=order.pk,
            validated_data=serializer.validated_data,
            user_id=request.user.pk,
        )

        serializer.save()
        return response.Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, order_id):
        order = get_object_or_404(models.Order, pk=order_id)
        # Needs to check why it doesn't work using self._check_users(...) !!!!
        if order.advertiser.id != request.user.pk:
            return response.Response({}, status=status.HTTP_403_FORBIDDEN)

        services.delete_order(order.pk)

        return response.Response({}, status=status.HTTP_204_NO_CONTENT)

    def patch(self, request, order_id):
        order = get_object_or_404(models.Order, pk=order_id)
        self._check_users(order.advertiser.id, request.user.pk)

        serializer = serializers.OrderPatchSerializer(
            instance=order, data=request.data
        )
        if not serializer.is_valid():
            return response.Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )

        services.update_order(
            order_id=order.pk,
            validated_data=serializer.validated_data,
            user_id=request.user.pk,
        )

        serializer.save()
        return response.Response(serializer.data, status=status.HTTP_200_OK)


class AdvertiserAPIView(views.APIView):
    @method_decorator(decorators.login_required)
    def get(self, request):
        advertiser = services.get_advertiser_by_id(request.user.pk)
        serializer = serializers.AdvertiserGetSerializer(advertiser)
        return response.Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = serializers.AdvertiserSerializer(data=request.data)
        if not serializer.is_valid():
            return response.Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )

        serializer.save()
        return response.Response(
            serializer.data, status=status.HTTP_201_CREATED
        )
