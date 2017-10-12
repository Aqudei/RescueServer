from rest_framework.generics import CreateAPIView
from rest_framework.views import APIView
from django.db.models import Count
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
            data['center'] = c
            data['num_evacuees'] = models.CheckIn.objects.filter(
                Incident=currentIncident, Center=c).count()
            data['num_members'] = c.members.count()
            datas.append(data)

        serializer = serializers.CenterMonitoringSerializer(datas, many=True)

        return Response(serializer.data,  status=status.HTTP_200_OK)


class MonitoringDetailAPIView(APIView):

    def get(self, request, pk=None):

        currentIncident = models.Incident.objects.get(IsActive=True)
        currentCenter = models.EvacuationCenter.objects.get(pk=pk)

        people_checked_in = models.CheckIn.objects.filter(
            Center=currentCenter, Incident=currentIncident)

        serializer = serializers.CheckInMonitoringSerializer(
            people_checked_in, many=True)
        return Response(serializer.data)


class PeopleReportAPIView(APIView):
    def get(self, request, incident=None):
        people = models.CheckIn.objects.filter(Incident=incident)
        serializer = serializers.PersonStatusSerializer(people, many=True)
        return Response(serializer.data)


class HouseholdsReportAPIView(APIView):
    def get(self, request, incident=None):
        houses = models.HouseholdStatus.objects.filter(
            Incident=incident).annotate(num_fam=Count('Household__members'))

        serializer = serializers.HouseStatusSerializer(houses, many=True)

        return Response(serializer.data)
