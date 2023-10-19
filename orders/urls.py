from django.urls import include, path
from .views import OrdersListCreate, OrderViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('', OrderViewSet, basename='orders')

urlpatterns = [
    path('', include(router.urls)),
]
