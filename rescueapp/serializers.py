from .models import CheckIn, EvacuationCenter,  Incident
from . import models
from rest_framework import serializers


class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Person
        fields = '__all__'


class PersonWriterSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Person
        exclude = ('Photo',)


class CenterSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.EvacuationCenter
        fields = '__all__'


class CenterWriterSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.EvacuationCenter
        exclude = ('Photo',)


class IncidentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Incident
        fields = '__all__'


class HouseholdSerializer(serializers.ModelSerializer):
    members = PersonSerializer(many=True, read_only=True)

    class Meta:
        model = models.Household
        fields = '__all__'


class PhotoSerializer(serializers.Serializer):
    Photo = serializers.ImageField()

class StatisticsSerializer(serializers.Serializer):
    NumberOfPerson = serializers.IntegerField(default=0)
    NumberOfHousehold = serializers.IntegerField(default=0)
    NumberOfEvacuation = serializers.IntegerField(default=0)
    NumberOfCalamities = serializers.IntegerField(default=0)
    