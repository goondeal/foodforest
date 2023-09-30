from django.shortcuts import get_object_or_404
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import RetrieveModelMixin, ListModelMixin

from .models import Country, State, City
from .serializers import CountrySerializer, StateSerializer, CitySerializer


class CountryViewSet(RetrieveModelMixin, ListModelMixin, GenericViewSet):
    model = Country
    lookup_field = 'code'
    lookup_url_kwarg = 'code'
    serializer_class = CountrySerializer
    queryset = Country.objects.filter(active=True)


class StateViewSet(RetrieveModelMixin, ListModelMixin, GenericViewSet):
    model = State
    serializer_class = StateSerializer

    def get_queryset(self):
        print('kwargs =', self.kwargs)
        country = get_object_or_404(Country, pk=self.kwargs.get('country_code'))
        return State.objects.filter(country=country, active=True)


class CityViewSet(RetrieveModelMixin, ListModelMixin, GenericViewSet):
    model = City
    serializer_class = CitySerializer

    def get_queryset(self):
        return City.objects.filter(state=self.kwargs.get('state_pk'), active=True)
