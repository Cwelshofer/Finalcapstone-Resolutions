"""Rare User Views Module"""
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework import serializers, status
from rest_framework.response import Response
from finalcapstoneapi.models import ResolutionUser

class ResolutionUsers(ViewSet):
    """RareUser Class"""

    def list(self, request):
        """ handles GET all"""
        users = ResolutionUser.objects.all()

        serializer = ResolutionUserSerializer(users, many=True, context={'request': request})
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single game
        Returns:
            Response -- JSON serialized game instance
        """
       
        try:
            user = ResolutionUser.objects.get(pk=pk)
            
            #logic to set an unmapped property on RareUser 
            #will let front end determine if the user retrieved by this function is the current user
            if request.auth.user.id == int(pk):
                user.is_current_user = True
            else:
                user.is_current_user = False

            serializer = ResolutionUserSerializer(user, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)
    

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'date_joined', 'is_staff', 'is_active', 'password')

class ResolutionUserSerializer(serializers.ModelSerializer):
    """Serializer for RareUser Info from a post"""
    user = UserSerializer(many=False)

    class Meta:
        model = ResolutionUser
        fields = ('id', 'bio', 'user', 'is_current_user')
