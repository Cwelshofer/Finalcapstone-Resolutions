"""Database RareUser module"""
from django.db import models
from django.contrib.auth.models import User


class ResolutionUser(models.Model):
    """RareUser database model"""
    bio = models.CharField(max_length=500)
    profile_image_url = models.CharField(max_length=500)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    @property
    def username(self):
        return self.user.username

    @property
    def is_current_user(self):
        return self.__is_current_user

    @is_current_user.setter
    def is_current_user(self,value):
        self.__is_current_user = value

