from rest_framework.generics import CreateAPIView
from rest_framework.views import APIView

from rest_framework.response import Response
from . import models
from . import serializers
from rest_framework import status
from django.db import models as djangomodels

NumberOfPerson = "NumberOfPerson"
NumberOfHousehold = "NumberOfHousehold"
NumberOfEvacuation = "NumberOfEvacuation"
NumberOfCalamities = "NumberOfCalamities"


class StatisticsAPIView(APIView):

    def get(self, request):
        stats = dict()

        stats[NumberOfPerson] = models.Person.objects.count()
        stats[NumberOfHousehold] = models.Household.objects.count()
        stats[NumberOfEvacuation] = models.EvacuationCenter.objects.count()
        stats[NumberOfCalamities] = models.Incident.objects.count()

        serializer = serializers.StatisticsSerializer(data=stats)
        if serializer.is_valid():
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MonitoringAPIView(APIView):

    def get(self, request):
        currentIncident = models.Incident.objects.get(IsActive=True)
        centers = models.EvacuationCenter.objects.all()
        datas = list()
        for c in centers:
            data = dict()
            data['center'] = c.__dict__
            data['num_evacuees'] = models.CheckIn.objects.filter(
                Incident=currentIncident, Center=c).count()
            datas.append(data)

        serializer = serializers.CenterMonitoringSerializer(
            data=datas, many=True)
        if serializer.is_valid():
            return Response(serializer.data,  status=status.HTTP_200_OK)
        else:
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MonitoringDetailAPIView(APIView):

    def get(self, request, pk=None):

        currentIncident = models.Incident.objects.get(IsActive=True)
        currentCenter = models.EvacuationCenter.objects.get(pk=pk)

        ids_person_chkin = models.CheckIn.objects.filter(
            Center=currentCenter, Incident=currentIncident).values_list(
                'Person', flat=True)

        persons_checked_in = models.Person.objects.filter(id__in=ids_person_chkin)

        data = dict()
        data['center'] = currentCenter
        data['persons'] = persons_checked_in

        serializer = serializers.DetailedMonitoringSerializer(data)

        return Response(serializer.data)
