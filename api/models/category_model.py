from django.db import models
import uuid

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