"""View module for handling requests about posts"""
from datetime import date
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.http import HttpResponseServerError
from rest_framework import serializers
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from finalcapstoneapi.models import Resolution, ResolutionUser, Category



class Resolutions(ViewSet):

    def list(self, request):

        resolutions = Resolution.objects.all()
        completed = self.request.query_params.get('completed', None)

        if not request.auth.user.is_staff:
            resolutions = resolutions.filter(approved = True)

        for resolution in resolutions:

            resolution.created_by_current_user = None

            if resolution.user.id == request.auth.user.id:
                resolution.created_by_current_user = True
            else:
                resolution.created_by_current_user = False

        user_id = self.request.query_params.get('user_id', None)
        if user_id is not None:
            resolutions = resolutions.filter(user_id=user_id)

        completed = self.request.query_params.get('completed', None)
        if completed is not None:
            resolutions = resolutions.filter(completed=completed)

        category_id = self.request.query_params.get('category_id', None)
        if category_id is not None:
            resolutions = resolutions.filter(category_id=category_id)
        
        serializer = ResolutionSerializer(
            resolutions, many=True, context={'request': request})
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single game
        Returns:
            Response -- JSON serialized game instance
        """
        try:
            resolution = Resolution.objects.get(pk=pk)
            if resolution.user.id == request.auth.user.id:
                resolution.created_by_current_user = True
            else:
                resolution.created_by_current_user = False
            serializer = ResolutionSerializer(resolution, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def create(self, request):
        """Handle POST operations
        Returns:
            Response -- JSON serialized resolution instance
        """
        user = request.auth.user
        resolution = Resolution()

        try:
            resolution.title = request.data["title"]
            resolution.content = request.data["content"]
            resolution.publication_date = request.data["publication_date"]
            resolution.completed = request.data["completed"]
        except KeyError as ex:
            return Response({'message': 'Incorrect key was sent in request'}, status=status.HTTP_400_BAD_REQUEST)

        resolution.user_id = user.id

        try:
            category = Category.objects.get(pk=request.data["category_id"])
            resolution.category_id = category.id
        except Category.DoesNotExist as ex:
            return Response({'message': 'Resolution type provided is not valid'}, status=status.HTTP_400_BAD_REQUEST)

        if user is not None:
            try:
                resolution.save()
                serializer = ResolutionSerializer(resolution, context={'request': request})
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except ValidationError as ex:
                return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)


    def update(self, request, pk=None):
        """Handle PUT requests for posts"""
       
        resolutionuser = ResolutionUser.objects.get(user=request.auth.user)

        resolution = Resolution.objects.get(pk=pk)
        resolution.title = request.data["title"]
        resolution.publication_date = request.data["publication_date"]
        resolution.content = request.data["content"]
        resolution.completed = request.data["completed"]
        resolution.user = resolutionuser

        category = Category.objects.get(pk=request.data["category_id"])
        resolution.category = category
        resolution.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)
        

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single post
        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            resolution = Resolution.objects.get(pk=pk)
            resolution.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Resolution.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(methods=['PUT'], detail=True)
    def approve(self, request, pk=None):

        resolution = Resolution.objects.get(pk=pk)

        resolution.completed = True
        resolution.save()
        
        return Response(None, status=status.HTTP_204_NO_CONTENT)
   






class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name',)

class ResolutionUserSerializer(serializers.ModelSerializer):
    """Serializer for ResolutionUser Info from a post"""
    user = UserSerializer(many=False)

    class Meta:
        model = ResolutionUser
        fields = ('id', 'bio', 'user')

class ResolutionSerializer(serializers.ModelSerializer):
    """Basic Serializer for a post"""
    user = ResolutionUserSerializer(many=False)

    class Meta:
        model = Resolution
        fields = ('id', 'title', 'publication_date', 'content',
                  'user', 'approved', 'category_id', 'image_url', 'created_by_current_user', 'completed')
        depth = 1
