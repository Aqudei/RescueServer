from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import detail_route
from .models import Person, CheckIn, EvacuationCenter, Incident, Household
from .serializers import PersonSerializer, CenterSerializer, HouseholdSerializer, PhotoSerializer
from rest_framework import status, response
# Create your views here.


class UploadMixin:
    @detail_route(methods=['patch', ])
    def upload(self, request, pk):
        photo = request.data['Photo']
        item = self.get_queryset().get(pk=pk)
        item.Photo = photo
        item.save()
        serializer = self.serializer_class(item)
        return response.Response(serializer.data)


class PersonViewSet(ModelViewSet, UploadMixin):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer


class CenterViewSet(ModelViewSet):
    queryset = EvacuationCenter.objects.all()
    serializer_class = CenterSerializer


class HouseholdViewSet(ModelViewSet):
    queryset = Household.objects.all()
    serializer_class = HouseholdSerializer
