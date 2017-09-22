from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .models import Person, CheckIn, EvacuationCenter, Incident, Household
from .serializers import PersonSerializer, CenterSerializer, HouseholdSerializer
# Create your views here.


class PersonViewSet(ModelViewSet):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer


class CenterViewSet(ModelViewSet):
    queryset = EvacuationCenter.objects.all()
    serializer_class = CenterSerializer


class HouseholdViewSet(ModelViewSet):
    queryset = Household.objects.all()
    serializer_class = HouseholdSerializer
