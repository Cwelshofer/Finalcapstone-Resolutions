"""PostTags Views Module"""
from django.core.exceptions import ValidationError
from rest_framework.viewsets import ViewSet
from rest_framework import serializers, status
from rest_framework.response import Response
from finalcapstoneapi.models import ResolutionTag, Tag, Resolution


class ResolutionTags(ViewSet):
    """ Responsible for GET, POST, DELETE """
    def list(self, request):
        """ GET all pt objects """
        resolutiontags = ResolutionTag.objects.all()

        resolution_id = self.request.query_params.get("resolution_id", None)
        tag_id = self.request.query_params.get("tag_id", None)

        if resolution_id is not None:
            resolutiontags = resolutiontags.filter(resolution_id=resolution_id)
        
        if tag_id is not None:
            resolutiontags = resolutiontags.filter(tag_id=tag_id)
        
        serializer = ResolutionTagSerializer(resolutiontags, many=True, context={'request', request})
        return Response(serializer.data)

    def create(self, request):
        """ POST """
        #these match the properties in PostForm.js
        resolution_id = request.data["resolution_id"]
        tag_id = request.data["tag_id"]

        #check if post exists
        try:
            resolution = Resolution.objects.get(id=resolution_id)
        except Resolution.DoesNotExist:
            return Response({'message: invalid resolution id'}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        
        #check if tag exists
        try:
            tag = Tag.objects.get(id=tag_id)
        except Tag.DoesNotExist:
            return Response({'message: invalid tag id'}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        
        #check if posttag exists
        try: 
            resolutiontag = ResolutionTag.objects.get(resolution=resolution, tag=tag)
            return Response({'message': 'Resolutiontag already exists for these two items'}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        except ResolutionTag.DoesNotExist:
            #if it does not exist, make new obj
            resolutiontag = ResolutionTag()
            resolutiontag.resolution = resolution
            resolutiontag.tag = tag
            try: 
                resolutiontag.save()
                serializer = ResolutionTagSerializer(resolutiontag, many=False, )
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except ValidationError as ex:
                return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        """ DELETE """
        try:
            resolutiontag = ResolutionTag.objects.get(pk=pk)
            resolutiontag.delete()
            return Response({}, status=status.HTTP_204_NO_CONTENT)
        except ResolutionTag.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ResolutionTagSerializer(serializers.ModelSerializer):
    """ Serializes PostTags """
    class Meta:
        model = ResolutionTag
        fields = ('id', 'tag_id', 'tag', 'resolution_id', 'resolution')
        depth = 3
        #so we can access whole tag and post object

