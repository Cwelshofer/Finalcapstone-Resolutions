"""Subscription model module"""
from django.db import models
# from . import RareUser


class Subscription(models.Model):
    """Subscription database model"""
    follower = models.ForeignKey("ResolutionUser", on_delete=models.CASCADE, related_name="follower")
    author = models.ForeignKey("ResolutionUser", on_delete=models.CASCADE, related_name="author")
    created_on = models.DateField(auto_now=False, auto_now_add=False)
    ended_on = models.DateField(auto_now=False, auto_now_add=False, null=True)
