from .models import CheckIn, EvacuationCenter,  Incident
from .models import Person, Household
from rest_framework import serializers


class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = '__all__'


class CenterSerializer(serializers.ModelSerializer):
    class Meta:
        model = EvacuationCenter
        fields = '__all__'


class IncidentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Incident
        fields = '__all__'


class HouseholdSerializer(serializers.ModelSerializer):
    class Meta:
        model = Household
        fields = '__all__'


class PhotoSerializer(serializers.Serializer):
    Photo = serializers.ImageField()
