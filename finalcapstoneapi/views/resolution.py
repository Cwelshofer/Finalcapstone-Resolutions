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
from finalcapstoneapi.models import Resolution, ResolutionUser



class Resolutions(ViewSet):

    def list(self, request):

        resolutions = Resolution.objects.all()

        if not request.auth.user.is_staff:
            resolutions = resolutions.filter(approved = True).filter(publication_date__lt=date.today())
            

        serializer = ResolutionSerializer(
            resolutions, many=True, context={'request': request})
        return Response(serializer.data)

    # def retrieve(self, request, pk=None):
    #     """Handle GET requests for single game
    #     Returns:
    #         Response -- JSON serialized game instance
    #     """
    #     try:
    #         post = Post.objects.get(pk=pk)
    #         if post.user.id == request.auth.user.id:
    #             post.created_by_current_user = True
    #         else:
    #             post.created_by_current_user = False
    #         serializer = PostSerializer(post, context={'request': request})
    #         return Response(serializer.data)
    #     except Exception as ex:
    #         return HttpResponseServerError(ex)

    # def create(self, request):
    #     """Handle POST operations
    #     Returns:
    #         Response -- JSON serialized post instance
    #     """
    #     user = request.auth.user
    #     post = Post()

    #     try:
    #         post.title = request.data["title"]
    #         post.content = request.data["content"]
    #         post.publication_date = request.data["publication_date"]
    #         post.image_url = request.data["image_url"]
        
    #     except KeyError as ex:
    #         return Response({'message': 'Incorrect key was sent in request'}, status=status.HTTP_400_BAD_REQUEST)

    #     post.user_id = user.id

    #     try:
    #         category = Category.objects.get(pk=request.data["category_id"])
    #         post.category_id = category.id
    #     except Category.DoesNotExist as ex:
    #         return Response({'message': 'Post type provided is not valid'}, status=status.HTTP_400_BAD_REQUEST)

    #     if user is not None:
    #         try:
    #             post.save()
    #             serializer = PostSerializer(post, context={'request': request})
    #             return Response(serializer.data, status=status.HTTP_201_CREATED)
    #         except ValidationError as ex:
    #             return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)


    # def update(self, request, pk=None):
    #     """Handle PUT requests for posts"""
       
    #     resolutionuser = ResolutionUser.objects.get(user=request.auth.user)

    #     post = Post.objects.get(pk=pk)
    #     post.title = request.data["title"]
    #     post.publication_date = request.data["publication_date"]
    #     post.content = request.data["content"]
    #     post.image_url = request.data["image_url"]
    #     post.user = resolutionuser

    #     category = Category.objects.get(pk=request.data["category_id"])
    #     post.category = category
    #     post.save()

    #     return Response({}, status=status.HTTP_204_NO_CONTENT)
        

    # def destroy(self, request, pk=None):
    #     """Handle DELETE requests for a single post
    #     Returns:
    #         Response -- 200, 404, or 500 status code
    #     """
    #     try:
    #         post = Post.objects.get(pk=pk)
    #         post.delete()

    #         return Response({}, status=status.HTTP_204_NO_CONTENT)

    #     except Post.DoesNotExist as ex:
    #         return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    #     except Exception as ex:
    #         return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # @action(methods=['PUT'], detail=True)
    # def approve(self, request, pk=None):

    #     post = Post.objects.get(pk=pk)

    #     post.approved = True
    #     post.save()
        
    #     return Response(None, status=status.HTTP_204_NO_CONTENT)






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
                  'user', 'approved', 'image_url', 'created_by_current_user')
        depth = 1
