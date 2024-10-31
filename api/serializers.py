from django.db.models import fields
from rest_framework import serializers
from .models import Item, User
 
class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ('id', 'category',  'name', 'amount')
        read_only_fields = ('id',)  # Make id read-only

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('name', 'id')

