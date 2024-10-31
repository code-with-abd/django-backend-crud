import uuid
from django.db import models
 
class Item(models.Model):
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
 
    def __str__(self) -> str:
        return self.name


class User(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self) -> str:
        return self.name