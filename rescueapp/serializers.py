from .models import CheckIn, EvacuationCenter,  Incident,  Person
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
