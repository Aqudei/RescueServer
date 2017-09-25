from rest_framework.generics import CreateAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from . import models
from . import serializers
from rest_framework import status


class ImageAPIView(APIView):

    def patch(self, request, pk):
        target_model = request.data['model']
        if target_model == 'Person':
            person = models.Person.objects.get(pk=int(pk))
            person.Photo = request.data['Photo']
            person.save()
            serializer = serializers.PersonSerializer(person.__dict__)

            return Response(serializer.data, status=status.HTTP_200_OK)
        elif target_model == 'Center':
            center = models.EvacuationCenter.objects.get(pk=int(pk))
            center.Photo = request.data['Photo']
            center.save()
            serializer = serializers.CenterSerializer(center)
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(status=status.HTTP_400_BAD_REQUEST)