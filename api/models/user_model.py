from django.db import models
from django.contrib.auth.models import User

class User(models.Model):
    name = models.CharField(max_length=30)
    username = models.CharField(max_length=30, default="default_username")

    def __str__(self) -> str:
        return self.name
