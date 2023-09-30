from django.shortcuts import get_object_or_404
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, ListModelMixin

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
        # First, check that the result includes only active restaurant
        queryset = Restaurant.objects.filter(active=True)
        # In case of retrieve action; url='/restaurants/{restaurant_slug}/',
        # leave the work for super().get_object() method
        if self.kwargs.get('slug'):
            return queryset
        
        # Else, the action is list url='/restaurants/?city={city_pk}', Filter by city 
        params = self.request.query_params
        print('kwargs =', self.kwargs)
        print('request.query_params =', params)
        cities_ids = [int(id) for id in params.getlist('city', [])]
        cities = City.objects.filter(pk__in=cities_ids)
        return Restaurant.objects.filter(city__in=cities)


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