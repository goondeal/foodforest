from django.db.models import Q
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListCreateAPIView
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST
from rest_framework.mixins import CreateModelMixin, UpdateModelMixin, RetrieveModelMixin, ListModelMixin
from rest_framework.viewsets import GenericViewSet
from restaurants.models import MenuItem, Restaurant
from .models import Order
from .serializers import OrderSerializer
from .permissions import CanOrder


class OrdersListCreate(ListCreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = (IsAuthenticated, CanOrder)
    queryset = Order.objects.all()

    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAuthenticated()]
        else:
            return [permission() for permission in self.permission_classes]

    def get_queryset(self):
        """
        This view should return a list of all the orders
        for the currently authenticated user.
        """
        user = self.request.user
        return Order.objects.filter(Q(user=user) | Q(phone=user.phone))

    def create(self, request):
        data = request.data
        data['user'] = request.user.id
        # check restaurant slug is provided
        r_slug = request.data.get('restaurant_slug')
        if r_slug:
            try:
                restaurant = Restaurant.objects.get(slug=r_slug)
                data['restaurant'] = restaurant.id
            except Restaurant.DoesNotExist:
                return Response(status=HTTP_400_BAD_REQUEST, data={'errors': "Restaurant not found"})
        else:
            return Response(status=HTTP_400_BAD_REQUEST, data={'errors': "Restaurant not provided"})

        # Check that order items are from that restaurant
        # Check that items list is not empty.
        items = request.data.get('items')
        if not items:
            return Response(status=HTTP_400_BAD_REQUEST, data={'errors': "Order must contain at least one item"})

        id = items[0].get('id')
        if id == None:
            return Response(status=HTTP_400_BAD_REQUEST, data={'errors': f"OrderItem {items[0].get('name')}: id not found"})
        first_item_obj = MenuItem.objects.get(pk=id)
        if not first_item_obj:
            return Response(status=HTTP_400_BAD_REQUEST, data={'errors': f"OrderItem {items[0].get('name')}: item not found"})

        if r_slug != first_item_obj.menu_category.restaurant.slug:
            return Response(status=HTTP_400_BAD_REQUEST, data={'errors': "OrderItems must belong to one restaurant(views)"})

        serializer = OrderFullSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
        else:
            return Response({
                "errors": serializer.errors
            })


class OrderViewSet(ListModelMixin, RetrieveModelMixin, CreateModelMixin, UpdateModelMixin, GenericViewSet):
    model = Order
    serializer_class = OrderSerializer
    permission_classes = (IsAuthenticated, CanOrder)

    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAuthenticated()]
        else:
            return [permission() for permission in self.permission_classes]

    def get_queryset(self):
        """
        This view should return a list of all the orders
        for the currently authenticated user.
        """
        user = self.request.user
        # return Order.objects.filter(Q(user=user) | Q(phone=user.phone))
        return Order.objects.filter(user=user)

    # def create(self, request, *args, **kwargs):
    #     # print('request data =', request.data)
    #     serializer = self.get_serializer(data=request.data)
    #     # print('\nserializer data = ', serializer.initial_data)
    #     serializer.is_valid(raise_exception=True)
    #     # print('\n serializer is valid \n')
    #     self.perform_create(serializer)
    #     headers = self.get_success_headers(serializer.data)
    #     from rest_framework import status
    #     return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)

    # def create(self, request):
    #     data = request.data
    #     data['user'] = request.user.id
    #     # check restaurant slug is provided
    #     r_slug = request.data.get('restaurant_slug')
    #     if r_slug:
    #         try:
    #             restaurant = Restaurant.objects.get(slug=r_slug)
    #             data['restaurant'] = restaurant.id
    #         except Restaurant.DoesNotExist:
    #             return Response(status=HTTP_400_BAD_REQUEST, data={'errors': "Restaurant not found"})
    #     else:
    #         return Response(status=HTTP_400_BAD_REQUEST, data={'errors': "Restaurant not provided"})

    #     # Check that order items are from that restaurant
    #     # Check that items list is not empty.
    #     items = request.data.get('items')
    #     if not items:
    #         return Response(status=HTTP_400_BAD_REQUEST, data={'errors': "Order must contain at least one item"})

    #     id = items[0].get('id')
    #     if id == None:
    #         return Response(status=HTTP_400_BAD_REQUEST, data={'errors': f"OrderItem {items[0].get('name')}: id not found"})
    #     first_item_obj = MenuItem.objects.get(pk=id)
    #     if not first_item_obj:
    #         return Response(status=HTTP_400_BAD_REQUEST, data={'errors': f"OrderItem {items[0].get('name')}: item not found"})

    #     if r_slug != first_item_obj.menu_category.restaurant.slug:
    #         return Response(status=HTTP_400_BAD_REQUEST, data={'errors': "OrderItems must belong to one restaurant(views)"})

    #     serializer = OrderFullSerializer(data=request.data)
    #     if serializer.is_valid(raise_exception=True):
    #         serializer.save()
    #         return Response(serializer.data)
    #     else:
    #         return Response({
    #             "errors": serializer.errors
    #         })

