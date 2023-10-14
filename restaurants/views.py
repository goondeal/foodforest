from django.shortcuts import get_object_or_404
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, ListModelMixin
from rest_framework import status
from rest_framework.response import Response
from .models import Restaurant, MenuItem, MenuCategory
from .serializers import *
from management.models import City


# User API
class RestaurantViewSet(CreateModelMixin, RetrieveModelMixin, ListModelMixin, GenericViewSet):
    model = Restaurant
    lookup_field = 'slug'
    lookup_url_kwarg = 'slug'
    serializer_class = RestaurantSerializer

    def get_queryset(self):
        queryset = Restaurant.objects.all()
        if self.request.method == 'POST':
            return queryset

        filters = {'active': True}
        # First, check that the result includes only active restaurant
        queryset = queryset.filter(**filters)
        # In case of retrieve action; url='/restaurants/{restaurant_slug}/',
        # leave the work for super().get_object() method
        if self.kwargs.get('slug'):
            return queryset

        # Else, the action is list url='/restaurants/?city={city_pk}', Filter by city
        params = self.request.query_params
        cities_ids = [int(id) for id in params.getlist('city', [])]
        if cities_ids:
            cities = City.objects.filter(pk__in=cities_ids)
            queryset = queryset.filter(city__in=cities)

        order_by = params.getlist('order_by', ['newest'])
        ORDER_BY_MODEL_ATTRS = {
            'newest': {'attr': 'created_at', 'desc': True},
            'name': {'attr': 'name'},
            'rating': {'attr': 'rating', 'desc': True},
            'num_reviews': {'attr': 'num_of_reviewers', 'desc': True}
        }
        ORDER_BY_OPTIONS = set(ORDER_BY_MODEL_ATTRS.keys())
        ORDER_BY_MODE = {'acc', 'desc'}
        print()
        print('order_by =', params.getlist('order_by', []))
        print('mode =', params.getlist('mode', []))
        if order_by and len(order_by) == 1 and order_by[0] in ORDER_BY_OPTIONS:
            ordering_mode = params.getlist('mode', [])
            ordering = ORDER_BY_MODEL_ATTRS.get(order_by[0]).get('attr')
            if ordering_mode and len(ordering_mode) == 1 and ordering_mode[0] in ORDER_BY_MODE:
                if ordering_mode[0] == 'desc':
                    ordering = '-' + ordering
            else:
                ordering = ORDER_BY_MODEL_ATTRS.get(order_by[0]).get('attr')
                if ORDER_BY_MODEL_ATTRS.get(order_by[0]).get('desc', False):
                    ordering = '-' + ordering

            print('ordering =', ordering)
            print()
            queryset = queryset.order_by(ordering)

        # print('queryset =', queryset.query)
        return queryset

    def create(self, request, *args, **kwargs):
        print('request data =', request.data)
        if request.user.is_authenticated:
            return super().create(request, *args, **kwargs)
        else:
            return Response({'message': 'Please, login first'}, status=status.HTTP_401_UNAUTHORIZED)

    def perform_create(self, serializer):
        print('creating restaurant with data =', serializer.validated_data)
        return serializer.save(owner=self.request.user)


class RestaurantMenu(ListModelMixin, GenericViewSet):
    model = MenuItem
    serializer_class = MenuItemSerializer

    def get_queryset(self):
        restaurant = get_object_or_404(
            Restaurant, slug=self.kwargs.get('restaurant_slug'))
        menu_categories = MenuCategory.objects.filter(restaurant=restaurant)
        return MenuItem.objects.filter(menu_category__in=menu_categories)

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class MenuCategoryViewSet(ModelViewSet):
    model = MenuCategory
    serializer_class = MenuCategorySerializer

    def get_queryset(self):
        restaurant = get_object_or_404(Restaurant, slug=self.kwargs.get('slug'))
        return restaurant.menu_categories.all()
