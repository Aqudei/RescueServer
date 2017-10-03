from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import detail_route
from . import models, serializers
from rest_framework import status, response
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
    def toggle_evacuation_membership(self, request, pk=None):
        person = self.get_object()
        center = models.EvacuationCenter.objects.get(
            pk=request.data['center_id'])

        if person._Center is not None and \
                person._Center == center:
            person._Center = None
        else:
            person._Center = center

        person.save()
        center.refresh_from_db()
        serializer = serializers.CenterSerializer(center)
        return response.Response(serializer.data)

    @detail_route(methods=['patch', ])
    def toggle_membership(self, request, pk=None):

        person = self.get_object()
        household = models.Household.objects.get(
            pk=request.data['household_id'])

        if person._Household is not None and \
                person._Household.id == household.id:
            person._Household = None
        else:
            person._Household = household

        person.save()

        household.refresh_from_db()
        serializer = serializers.HouseholdSerializer(household)
        return response.Response(serializer.data)

    @detail_route(methods=['post', ])
    def check_in(self, request, pk=None):

        person = self.get_object()
        incident = models.Incident.objects.filter(
            IsActive=True).first()

        if incident is not None:
            center = person._Center

            if(models.CheckIn.objects.filter(
                    Incident=incident, Person=person).exists() == False):

                checkin = models.CheckIn.objects.create(
                    Incident=incident,
                    Person=person,
                    Center=center
                )

                center.refresh_from_db()
                data = dict()
                data['center'] = center
                data['num_evacuees'] = models.CheckIn.objects.filter(
                    Incident=incident, Center=center).count()

                serializer = serializers.CenterMonitoringSerializer(
                    data)

                #serializer = serializers.IncidentSerializer(incident)
                return response.Response(serializer.data)
            else:
                return response.Response(status=status.HTTP_400_BAD_REQUEST)

        return response.Response(status=status.HTTP_400_BAD_REQUEST)


class CenterViewSet(MultiSerializerViewSetMixin, UploadMixin,  ModelViewSet):
    queryset = models.EvacuationCenter.objects.all()
    serializer_class = serializers.CenterSerializer

    serializer_action_classes = {
        'create': serializers.CenterWriterSerializer,
        'update': serializers.CenterWriterSerializer,
        'partial_update': serializers.CenterWriterSerializer,
    }


class HouseholdViewSet(ModelViewSet, UploadMixin):
    queryset = models.Household.objects.all()
    serializer_class = serializers.HouseholdSerializer


class IncidentsViewSet(ModelViewSet):
    queryset = models.Incident.objects.all()
    serializer_class = serializers.IncidentSerializer

    serializer_action_classes = {
        'create': serializers.IncidentWriterSerializer,
        'update': serializers.IncidentWriterSerializer,
    }

    @detail_route(methods=['patch', ])
    def set_active(self, request, pk=None):

        incident2 = self.get_object()
        incident = models.Incident.objects.filter(
            IsActive=True).first()

        if incident is None:
            incident2.IsActive = True
            incident2.save()
            serializer = serializers.IncidentSerializer(incident2)
            return response.Response(serializer.data)
        else:
            if not incident == incident2:
                incident.IsActive = False
                incident2.IsActive = True
                incident.save()
                incident2.save()

                incidents = models.Incident.objects.filter(
                    id__in=[incident.id, incident2.id])

                serializer = serializers.IncidentSerializer(
                    incidents, many=True)

                return response.Response(serializer.data)

        return response.Response()

    @detail_route(methods=['patch', ])
    def toggle(self, request, pk=None):

        current_incident = self.get_object()
        desired = not current_incident.IsActive

        # deactivate
        if desired == False:
            current_incident.IsActive = False
            current_incident.save()
            serializer = serializers.IncidentSerializer(current_incident)
            return response.Response(serializer.data)
        else:
            return self.set_active(request, pk)
