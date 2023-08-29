from django.urls import include, path, register_converter
from rest_framework.routers import DefaultRouter
from .views import RestaurantViewSet
from .custom_slug_converter import CustomSlugConverter


register_converter(CustomSlugConverter, 'custom_slug')

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'', RestaurantViewSet, basename='restaurant')

urlpatterns = [
    path('', include(router.urls)),
    # path('<custom_slug:slug>/', RestaurantDetail.as_view()),
    # path('<custom_slug:slug>/menu/', RestaurantMenu.as_view()),
]
