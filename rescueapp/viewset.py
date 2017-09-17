from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .models import Person, CheckIn, EvacuationCenter, Incident
from .serializers import PersonSerializer, CenterSerializer
# Create your views here.


class PersonViewSet(ModelViewSet):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer

class CenterViewSet(ModelViewSet):
    queryset = EvacuationCenter.objects.all()
    serializer_class = CenterSerializer