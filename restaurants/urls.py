from django.urls import include, path, register_converter
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers
from .views import RestaurantViewSet, RestaurantMenu
from .custom_slug_converter import CustomSlugConverter


register_converter(CustomSlugConverter, 'custom_slug')

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'', RestaurantViewSet, basename='restaurant')

restaurant_router = routers.NestedDefaultRouter(
    router,
    r'',
    lookup='restaurant'
)
restaurant_router.register(r'menu', RestaurantMenu, basename='restaurant-menu')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(restaurant_router.urls)),
    # path('<custom_slug:slug>/', RestaurantDetail.as_view()),
    # path('<custom_slug:slug>/menu/', RestaurantMenu.as_view()),
]
