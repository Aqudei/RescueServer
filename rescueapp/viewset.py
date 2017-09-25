from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import detail_route
from . import models, serializers
from rest_framework import status, response
import json
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
    queryset = models.Person.objects.all()
    serializer_class = serializers.PersonSerializer


class CenterViewSet(ModelViewSet):
    queryset = models.EvacuationCenter.objects.all()
    serializer_class = serializers.CenterSerializer


class HouseholdViewSet(ModelViewSet):
    queryset = models.Household.objects.all()
    serializer_class = serializers.HouseholdSerializer


class IncidentsViewSet(ModelViewSet):
    queryset = models.Incident.objects.all()
    serializer_class = serializers.IncidentSerializer

    @detail_route(methods=['patch', ])
    def set_active(self, request, pk=None):
     
        incident = models.Incident.objects.filter(IsActive=True).first()
        if incident is not None:
            incident.IsActive = False
            incident.save()

        incident2 = models.Incident.objects.get(id=pk)
        incident2.IsActive = True
        incident2.save()

        incidents = models.Incident.objects.filter(
            id__in=[incident.id, incident2.id])
        print(incidents)
        serializer = serializers.IncidentSerializer(data=incidents, many=True)
        serializer.is_valid()
        return response.Response(serializer.data)
    