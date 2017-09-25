from rest_framework.generics import CreateAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from . import models
from . import serializers
from rest_framework import status

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
