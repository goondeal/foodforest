from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, ListModelMixin

from .models import Restaurant
from .serializers import *
from .permissions import RestaurantPermission


# API
class RestaurantViewSet(
        CreateModelMixin,
        RetrieveModelMixin,
        ListModelMixin,
        GenericViewSet
):

    model = Restaurant
    lookup_field = 'slug'
    slug_field = 'slug'
    serializer_class = RestaurantSerializer
    permission_classes = [RestaurantPermission]
    queryset = Restaurant.objects.all()


    # menu_categories = restaurant.menu_categories.all()
    # serializer = MenuCategorySerializer(menu_categories, many=True)
    # return Response(serializer.data)
