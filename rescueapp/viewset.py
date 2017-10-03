from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import detail_route
from . import models, serializers
from rest_framework import status, response, exceptions
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
        return response.Response(
            serializer.data, status=status.HTTP_200_OK)


class MultiSerializerViewSetMixin(object):
    def get_serializer_class(self):
        """
        Look for serializer class in self.serializer_action_classes, which
        should be a dict mapping action name (key) to serializer class (value),
        i.e.:

        class MyViewSet(MultiSerializerViewSetMixin, ViewSet):
            serializer_class = MyDefaultSerializer
            serializer_action_classes = {
               'list': MyListSerializer,
               'my_action': MyActionSerializer,
            }

            @action
            def my_action:
                ...

        If there's no entry for that action then just fallback to the regular
        get_serializer_class lookup: self.serializer_class, DefaultSerializer.

        Thanks gonz: http://stackoverflow.com/a/22922156/11440

        """
        try:
            return self.serializer_action_classes[self.action]
        except (KeyError, AttributeError):
            return super(MultiSerializerViewSetMixin, self).get_serializer_class()


class PersonViewSet(ModelViewSet, UploadMixin):
    queryset = models.Person.objects.all()
    serializer_class = serializers.PersonSerializer

    @detail_route(methods=['patch', ])
    def toggle_membership(self, request, pk=None):

        person = self.get_object()
        household = models.Household.objects.get(
            pk=request.data['household_id'])

        desired = not household.members.filter(id=person.id).exists()

        if desired:
            if household.members.filter(IsHead=True).exists() and person.IsHead:
                raise exceptions.ValidationError(
                    detail=["household already has a head family.", ], code=status.HTTP_400_BAD_REQUEST)

        if person._Household is not None and \
                person._Household.id == household.id:
            person._Household = None
        else:
            person._Household = household

        person.save()

        household.refresh_from_db()
        serializer = serializers.HouseholdSerializer(household)
        return response.Response(serializer.data)

    @detail_route
    def check_in(self, request, pk=None):

        person = self.get_object()
        incident = models.Incident.objects.filter(
            IsActive=True).first()

        if incident is not None:
            center = person._Center

            checkin = models.CheckIn.objects.create(
                Incident=incident,
                Person=person,
                center=center
            )

            serializer = serializers.IncidentSerializer(data=incident)
            if serializer.is_valid():
                return response.Response(serializer.data)
            else:
                return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return response.Response(status=status.HTTP_400_BAD_REQUEST)


class CenterViewSet(MultiSerializerViewSetMixin, UploadMixin,  ModelViewSet):
    queryset = models.EvacuationCenter.objects.all()
    serializer_class = serializers.CenterSerializer

    serializer_action_classes = {
        'create': serializers.CenterWriterSerializer,
        'update': serializers.CenterWriterSerializer,
    }


class HouseholdViewSet(ModelViewSet, UploadMixin):
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
        serializer = serializers.IncidentSerializer(
            data=incidents, many=True)
        serializer.is_valid()
        return response.Response(serializer.data)
