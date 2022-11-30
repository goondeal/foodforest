from django.http import Http404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from .models import Restaurant, MenuCategory
from .serializers import *


# API
class RestaurantList(ListAPIView):
    """
    List all restaurants in the home page.
    """
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantShallowSerializer
    # def get(self, request, format=None):
    #     restaurants = Restaurant.objects.all()
    #     serializer = RestaurantShallowSerializer(restaurants, many=True)
    #     return Response(serializer.data)


class RestaurantDetail(APIView):
    """
    Retrieve restaurant data for Restaurant page.
    """
    model = Restaurant
    slug_field = 'slug'
    serializer = RestaurantFullSerializer

    def get_object(self, slug):
        try:
            return Restaurant.objects.get(slug=slug)
        except Restaurant.DoesNotExist:
            raise Http404

    def get(self, request, slug, format=None):
        snippet = self.get_object(slug)
        serializer = RestaurantFullSerializer(snippet)
        return Response(serializer.data)


class RestaurantMenu(APIView):
    """
    Retrieve restaurant menu showd in the restaurant page if the restaurant is open.
    """
    model = MenuCategory
    slug_field = 'slug'

    def get(self, request, slug, format=None):
        try:
            restaurant = Restaurant.objects.get(slug=slug)
            menu_categories = restaurant.menu_categories.all()
            serializer = MenuCategorySerializer(menu_categories, many=True)
            return Response(serializer.data)
        except Restaurant.DoesNotExist:
            raise Http404
