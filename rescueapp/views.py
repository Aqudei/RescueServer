from rest_framework.generics import CreateAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from . import models, serializers
from rest_framework import status


class ImageAPIView(APIView):

    def patch(self, request, pk):
        target_model = request.data['model']
        if target_model == 'Person':
            person = models.Person.objects.get(pk=int(pk))
            person.Photo = request.data['Photo']
            person.save()
            person.refresh_from_db()
            serialized = serializers.PersonSerializer(person)
            return Response(serialized.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)
