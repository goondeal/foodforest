from django.urls import include, path
from rest_framework_nested import routers
from .views import CountryViewSet, StateViewSet, CityViewSet


router = routers.DefaultRouter()
router.register(r'countries', CountryViewSet, basename='country')
# generates:
# /countries/
# /countries/{code}/
countries_router = routers.NestedDefaultRouter(
    router,
    r'countries',
    lookup='country'
)
countries_router.register(
    r'states',
    StateViewSet,
    basename='country-states'
)
# generates:
# /countries/{code}/states/
# /countries/{code}/states/{pk}/
states_router = routers.NestedDefaultRouter(
    countries_router, r'states', lookup='state')
states_router.register(r'cities', CityViewSet, basename='state-cities')
# generates:
# /countries/{code}/states/{pk}/cities/
# /countries/{code}/states/{pk}/cities/{pk}/


urlpatterns = [
    path('', include(router.urls)),
    path('', include(countries_router.urls)),
    path('', include(states_router.urls)),
]
