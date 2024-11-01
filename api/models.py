import uuid
from django.db import models

 
class Item(models.Model, models.File):
    id = models.CharField(
        max_length=36,
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        unique=True
    )
    
    category = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    amount = models.PositiveIntegerField()
    picture = models.ImageField(upload_to='item_pictures/', null=True, blank=True)  # New field
 
    def __str__(self) -> str:
        return self.name


class User(models.Model):
    name = models.CharField(max_length=30)
    username = models.CharField(max_length=30, default="default_username")

    def __str__(self) -> str:
        return self.name