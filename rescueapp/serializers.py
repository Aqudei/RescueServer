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
    members = PersonSerializer(many=True, read_only=True)

    class Meta:
        model = models.EvacuationCenter
        fields = '__all__'


class SimplePersonSerializer(serializers.ModelSerializer):

    _Household = serializers.SlugRelatedField(
        many=False,
        read_only=True,
        slug_field='HouseNumber'
    )

    class Meta:
        model = models.Person
        fields = (
            'NameSuffix', 'FirstName',
            'MiddleName', 'LastName',
            'Birthday', '_Household'
        )


class TheVulnerablesSerializer(serializers.ModelSerializer):

    _Household = serializers.SlugRelatedField(
        many=False,
        read_only=True,
        slug_field='Address'
    )

    class Meta:
        model = models.Person
        fields = (
            'NameSuffix', 'FirstName',
            'MiddleName', 'LastName',
            'Birthday', '_Household', 'Gender'
        )


class PersonStatusSerializer(serializers.ModelSerializer):
    Person = SimplePersonSerializer(many=False, read_only=True)

    class Meta:
        model = models.CheckIn
        exclude = ('Incident',)


class HouseStatusSerializer(serializers.ModelSerializer):
    num_fam = serializers.IntegerField(read_only=True)
    Household = serializers.SlugRelatedField(
        many=False,
        read_only=True,
        slug_field='HouseNumber'
    )

    family_head = serializers.CharField(read_only=True)

    class Meta:
        model = models.HouseholdStatus
        fields = '__all__'


class CenterWriterSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.EvacuationCenter
        exclude = ('Photo',)


class CenterMonitoringSerializer(serializers.Serializer):
    num_members = serializers.IntegerField(read_only=True)
    center = CenterWriterSerializer(read_only=False, many=False)
    num_evacuees = serializers.IntegerField()


class PersonIdSerializer(serializers.ModelSerializer):

    Status = serializers.CharField(read_only=True)

    class Meta:
        model = models.Person
        fields = ('id',)


class DetailedMonitoringSerializer(serializers.Serializer):
    center = CenterSerializer(read_only=True)
    persons = PersonIdSerializer(
        many=True, read_only=True)


class IncidentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Incident
        fields = '__all__'


class IncidentWriterSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Incident
        exclude = ('Photo', 'DateOccured', 'IsActive')


class HouseholdSerializer(serializers.ModelSerializer):
    members = PersonSerializer(many=True, read_only=True)

    class Meta:
        model = models.Household
        fields = '__all__'


class HouseholdsInDangerZoneSerializer(serializers.ModelSerializer):
    family_head = serializers.CharField(read_only=True)
    num_fam = serializers.IntegerField()
    num_vulnerable = serializers.IntegerField()

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


class CheckInSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = models.CheckIn


class PersonIdAndNameSerializer(serializers.ModelSerializer):

    fullname = serializers.CharField(read_only=True)

    class Meta:
        model = models.Person
        fields = ('id', 'fullname')


class CenterWithMembersSerializer(serializers.ModelSerializer):
    members = PersonIdAndNameSerializer(read_only=True, many=True)

    class Meta:
        model = models.EvacuationCenter
        fields = ('members',)


class CheckInMonitoringSerializer(serializers.ModelSerializer):

    fullname = serializers.CharField(
        read_only=True, source='Person.fullname'
    )

    class Meta:
        exclude = ('id',)
        model = models.CheckIn


class TollSerializer(serializers.Serializer):
    Status = serializers.CharField()
    count = serializers.IntegerField()
