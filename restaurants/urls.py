from django.urls import include, path, register_converter
from rest_framework_nested import routers
from .views import RestaurantViewSet, RestaurantAdminViewSet, MenuCategoryAdminViewSet, MenuItemsAdminViewSet
from .custom_slug_converter import CustomSlugConverter


register_converter(CustomSlugConverter, 'custom_slug')

router = routers.DefaultRouter()
router.register(r'', RestaurantViewSet, basename='restaurant')
# generates:
# /restaurants/
# /restaurants/{slug}/


restaurant_router = routers.NestedDefaultRouter(router, r'', lookup='restaurant')
restaurant_router.register(r'menu', MenuCategoryAdminViewSet, basename='menu')

menu_router = routers.NestedDefaultRouter(restaurant_router, r'menu', lookup='menu_category')
menu_router.register(r'items', MenuItemsAdminViewSet, basename='items')


urlpatterns = [
    path('', include(router.urls)),
    path('', include(restaurant_router.urls)),
    path('', include(menu_router.urls)),
    # path('<custom_slug:slug>/', include),
]
