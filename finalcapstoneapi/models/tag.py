"""Tag model module"""
from django.db import models


class Tag(models.Model):
    """Tag database model"""
    label = models.CharField(max_length=25)
