from .models import CheckIn, EvacuationCenter,  Incident
from .models import Person, Household
from rest_framework.serializers import ModelSerializer


class PersonSerializer(ModelSerializer):
    class Meta:
        model = Person
        fields = '__all__'


class CenterSerializer(ModelSerializer):
    class Meta:
        model = EvacuationCenter
        fields = '__all__'


class IncidentSerializer(ModelSerializer):
    class Meta:
        model = Incident
        fields = '__all__'


class HouseholdSerializer(ModelSerializer):
    class Meta:
        model = Household
        fields = '__all__'
