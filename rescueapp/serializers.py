from .models import CheckIn, EvacuationCenter,  Incident
from . import models 
from rest_framework import serializers


class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Person
        fields = '__all__'


class CenterSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.EvacuationCenter
        fields = '__all__'


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
