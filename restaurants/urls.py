from django.urls import path, register_converter
from .views import RestaurantList, RestaurantDetail, RestaurantMenu
from .custom_slug_converter import CustomSlugConverter

register_converter(CustomSlugConverter, 'custom_slug')
urlpatterns = [
    path('', RestaurantList.as_view()),
    path('<custom_slug:slug>/', RestaurantDetail.as_view()),
    path('<custom_slug:slug>/menu/', RestaurantMenu.as_view()),
]
