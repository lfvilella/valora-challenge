from django.utils.decorators import method_decorator
from django.contrib.auth import decorators

from rest_framework import authentication
from rest_framework import views
from rest_framework import response
from rest_framework import status
from rest_framework import permissions

from . import serializers, services


class CsrfExemptSessionAuthentication(authentication.SessionAuthentication):
    def enforce_csrf(self, request):
        pass


class RestBaseView(views.APIView):
    authentication_classes = [
        authentication.BasicAuthentication,
        CsrfExemptSessionAuthentication,
    ]


class UserAuthView(RestBaseView):

    def post(self, request):
        serializer = serializers.UserLoginSerializer(data=request.data)

        if not serializer.is_valid():
            return response.Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )

        user = services.user_login(
            request,
            username=serializer.data["username"],
            password=serializer.data["password"],
        )
        user_detail = serializers.UserDetailSerializer(user)

        return response.Response(user_detail.data, status=status.HTTP_200_OK)

    def delete(self, request):
        services.user_logout(request)
        return response.Response({}, status=status.HTTP_204_NO_CONTENT)


class OrderAPIView(RestBaseView):

    permission_classes = [permissions.IsAuthenticated]

    def _detail(self, request, order_id):
        order = services.get_order(order_id, request.user.pk)
        if not order:
            return response.Response({}, status=status.HTTP_404_NOT_FOUND)

        serializer = serializers.OrderSerializer(order)
        return response.Response(serializer.data, status=status.HTTP_200_OK)

    def _list(self, request):
        orders = services.list_order(request.user.pk)
        serialized_orders = []
        for order in orders:
            serializer = serializers.OrderSerializer(order)
            serialized_orders.append(serializer.data)

        return response.Response(serialized_orders, status=status.HTTP_200_OK)

    def get(self, request, order_id=None):
        if order_id:
            return self._detail(request, order_id)
        return self._list(request)

    def post(self, request):
        serializer = serializers.OrderCreateSerializer(data=request.data)
        if not serializer.is_valid():
            return response.Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )

        order = services.create_order(
            validated_data=serializer.validated_data, user_id=request.user.pk
        )
        serializer = serializers.OrderSerializer(order)
        return response.Response(
            serializer.data, status=status.HTTP_201_CREATED
        )

    def put(self, request, order_id):
        order = services.get_order(order_id, request.user.pk)
        if not order:
            return response.Response({}, status=status.HTTP_404_NOT_FOUND)

        serializer = serializers.OrderSerializer(
            instance=order, data=request.data
        )
        if not serializer.is_valid():
            return response.Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )

        updated_order = services.update_order(
            order_id=order.pk,
            validated_data=serializer.validated_data,
            user_id=request.user.pk,
        )
        serializer = serializers.OrderSerializer(updated_order)

        return response.Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, order_id):
        deleted_order = services.delete_order(order_id, request.user.pk)
        if not deleted_order:
            return response.Response({}, status=status.HTTP_404_NOT_FOUND)

        serializer = serializers.OrderSerializer(deleted_order)
        return response.Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, order_id):
        order = services.get_order(order_id, request.user.pk)
        if not order:
            return response.Response({}, status=status.HTTP_404_NOT_FOUND)

        serializer = serializers.OrderPatchSerializer(
            instance=order, data=request.data
        )
        if not serializer.is_valid():
            return response.Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )

        updated_order = services.update_order(
            order_id=order.pk,
            validated_data=serializer.validated_data,
            user_id=request.user.pk,
        )
        serializer = serializers.OrderSerializer(updated_order)

        return response.Response(serializer.data, status=status.HTTP_200_OK)


class AdvertiserAPIView(RestBaseView):
    @method_decorator(decorators.login_required)
    def get(self, request):
        advertiser = services.get_advertiser_by_user_id(request.user.pk)
        serializer = serializers.AdvertiserGetSerializer(advertiser)
        return response.Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = serializers.AdvertiserSerializer(data=request.data)
        if not serializer.is_valid():
            return response.Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )

        advertiser = serializer.save()

        services.user_login(
            request,
            username=request.data["user"]["username"],
            password=request.data["user"]["password"],
        )

        serializer = serializers.AdvertiserGetSerializer(advertiser)
        return response.Response(
            serializer.data, status=status.HTTP_201_CREATED
        )
