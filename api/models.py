import uuid
from django.db import models
from django.contrib.auth.models import User

 
class Item(models.Model):
    id = models.CharField(
        max_length=36,
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        unique=True
    )
    
    category = models.ForeignKey(
        "Category", on_delete=models.CASCADE
    )

    
    createdBy = models.ForeignKey(
       User, on_delete=models.CASCADE
    )

    name = models.CharField(max_length=255)
    amount = models.PositiveIntegerField()
    units = models.PositiveIntegerField()
    picture = models.ImageField(upload_to='item_pictures/', null=True, blank=True)  # New field
 
    def __str__(self) -> str:
        return self.name


class User(models.Model):
    name = models.CharField(max_length=30)
    username = models.CharField(max_length=30, default="default_username")

    def __str__(self) -> str:
        return self.name
    


class Category(models.Model):
    name = models.CharField(max_length=30)
    id = models.CharField(
        max_length=36,
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        unique=True
    )
    def __str__(self) -> str:
        return self.name