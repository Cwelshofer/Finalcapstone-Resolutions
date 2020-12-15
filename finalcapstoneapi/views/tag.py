"""Tag Views Module"""
from django.core.exceptions import ValidationError
from rest_framework.viewsets import ViewSet
from rest_framework import serializers, status
from rest_framework.response import Response
from finalcapstoneapi.models import Tag


class Tags(ViewSet):
    """Tags Class"""

    def list(self, request):
        """ handles GET all"""
        tags = Tag.objects.all()

        resolution_id = self.request.query_params.get('resolution_id', None)
        if resolution_id is not None:
            tags = tags.filter(resolution_id=resolution_id)


        serializer = TagSerializer(tags, many=True, context={'request': request})
        return Response(serializer.data)

    def create(self, request):
        """ handles POST """
        tag = Tag()
        tag.label = request.data["label"]

        try:
            tag.save()
            serializer = TagSerializer(tag, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single game
        Returns:
            Response -- JSON serialized game instance
        """
        try:
            tag = Tag.objects.get(pk=pk)
            serializer = TagSerializer(tag, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single post
        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            tag = Tag.objects.get(pk=pk)
            tag.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Tag.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update(self, request, pk=None):
        """Handle PUT requests for posts"""

        tag = Tag.objects.get(pk=pk)
        tag.label = request.data["label"]
        tag.save()

       

        return Response({}, status=status.HTTP_204_NO_CONTENT)


class TagSerializer(serializers.ModelSerializer):
    """ Tag Serializer """
    class Meta:
        model = Tag
        fields = ('id', 'label')