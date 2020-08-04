""" Views

This module is responsible to handle all interactions to the API.
"""

from django.utils.decorators import method_decorator
from django.contrib.auth import decorators

from rest_framework import authentication
from rest_framework import views
from rest_framework import response
from rest_framework import status
from rest_framework import permissions

from . import serializers, services


class CsrfExemptSessionAuthentication(authentication.SessionAuthentication):
    """ CSRF Exempt Session Authentication

    Note:
        The purpose of it is disable the CSRF token.
    """

    def enforce_csrf(self, request):
        """ Enforce CSRF.

        Args:
            request: Request.
        """
        pass


class RestBaseView(views.APIView):
    """ Rest Base View

    It is responsible to authentication.
    """

    authentication_classes = [
        authentication.BasicAuthentication,
        CsrfExemptSessionAuthentication,
    ]


class UserAuthView(RestBaseView):
    """ User Auth View

    It is responsible to authenticate User.
    """

    def post(self, request):
        """ User Login

        Args:
            request: Request.

        Returns:
            - serializers.UserDetailSerializer + HTTP_200_OK if request.data
            is valid.
            - serializer.errors + HTTP_400_BAD_REQUEST if request.data
            is not valid.
        """

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
        """ User Logout

        Args:
            request: Request.

        Returns:
            - HTTP_204_NO_CONTENT
        """

        services.user_logout(request)
        return response.Response({}, status=status.HTTP_204_NO_CONTENT)


class OrderAPIView(RestBaseView):
    """ Order API View

    It is responsible to handle orders API.
    """

    permission_classes = [permissions.IsAuthenticated]

    def _detail(self, request, order_id: int):
        """ Get Order

        Args:
            request: Request.
            order_id: Order ID.

        Returns:
            - serializers.OrderSerializer + HTTP_200_OK if request.data
            is valid.
            - HTTP_404_BAD_REQUEST if request.data or user/advertiser
            is not valid.
        """
        order = services.get_order(order_id, request.user.pk)
        if not order:
            return response.Response({}, status=status.HTTP_404_NOT_FOUND)

        serializer = serializers.OrderSerializer(order)
        return response.Response(serializer.data, status=status.HTTP_200_OK)

    def _list(self, request):
        """ List Orders

        Args:
            request: Request.

        Returns:
            - typing.List[serializers.OrderSerializer] + HTTP_200_OK if
            user/advertiser has orders.
            - Empity List [] if user/advertiser  has no orders.
        """

        orders = services.list_orders(request.user.pk)
        serialized_orders = []
        for order in orders:
            serializer = serializers.OrderSerializer(order)
            serialized_orders.append(serializer.data)

        return response.Response(serialized_orders, status=status.HTTP_200_OK)

    def get(self, request, order_id: int = None):
        """ Handle Get Request

        Returns:
            - Order Detail if request is about a specific order.
            - List Orders if request has no order_id.
        """

        if order_id:
            return self._detail(request, order_id)
        return self._list(request)

    def post(self, request):
        """ Create Order

        Args:
            request: Request.

        Returns:
            - serializers.OrderSerializer + HTTP_200_OK if request.data
            is valid.
            - serializer.errors + HTTP_400_BAD_REQUEST if request.data
            is not valid.
        """

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

    def put(self, request, order_id: int):
        """ Update Order

        Args:
            request: Request.
            order_id: Order ID.

        Returns:
            - serializers.OrderSerializer + HTTP_200_OK if request.data
            is valid.
            - HTTP_404_NOT_FOUND if has no order.
            - serializer.errors + HTTP_400_BAD_REQUEST if request.data
            is not valid.
        """

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

    def delete(self, request, order_id: int):
        """ Delete Order

        Args:
            request: Request.
            order_id: Order ID.

        Returns:
            - serializers.OrderSerializer + HTTP_200_OK if request.data
            is valid.
            - HTTP_404_NOT_FOUND if has no order.
        """

        deleted_order = services.delete_order(order_id, request.user.pk)
        if not deleted_order:
            return response.Response({}, status=status.HTTP_404_NOT_FOUND)

        serializer = serializers.OrderSerializer(deleted_order)
        return response.Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, order_id: int):
        """ Patch Order

        Args:
            request: Request.
            order_id: Order ID.

        Returns:
            - serializers.OrderSerializer + HTTP_200_OK if request.data
            is valid.
            - HTTP_404_NOT_FOUND if has no order.
            - serializer.errors + HTTP_400_BAD_REQUEST if request.data
            is not valid.
        """

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
    """ Advertiser API View

    It is responsible to handle advertiser API.
    """

    @method_decorator(decorators.login_required)
    def get(self, request):
        """ Get Advertiser/User logged

        Args:
            request: Request.

        Returns:
            - serializers.AdvertiserGetSerializer + HTTP_200_OK
        """
        advertiser = services.get_advertiser_by_user_id(request.user.pk)
        serializer = serializers.AdvertiserGetSerializer(advertiser)
        return response.Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        """ Create Advertiser

        Args:
            request: Request.

        Returns:
            - serializers.AdvertiserGetSerializer + HTTP_200_OK if
            request.data is valid.
            - serializer.errors + HTTP_400_BAD_REQUEST if request.data
            is not valid.
        """

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
