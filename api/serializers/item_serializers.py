from rest_framework import serializers
from django.contrib.auth.models import User

from api.serializers.category_serializer import CategorySerializer
from ..models.items_model import Item
from ..models.category_model import Category
from .user_serializer import UserSerializer

class ItemSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
    createdBy = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Item
        fields = ('id', 'category', 'name', 'amount', 'picture', 'createdBy', 'units')
        read_only_fields = ('id',)

    def to_representation(self, instance):
        # Call the default representation
        representation = super().to_representation(instance)
        
        # Replace 'category' with its serialized data
        representation['category'] = CategorySerializer(instance.category).data
        
        # Replace 'createdBy' with its serialized data
        representation['createdBy'] = UserSerializer(instance.createdBy).data
        return representation

    def to_internal_value(self, data):
        data = super().to_internal_value(data)
        
        # Validate 'amount' if it exists
        if 'amount' in data:
            try:
                data['amount'] = int(data['amount'])  # Convert amount to integer
            except ValueError:
                raise serializers.ValidationError({"amount": "Amount must be a valid number."})
        
        # Validate 'units' if it exists
        if 'units' in data:
            try:
                data['units'] = int(data['units'])  # Convert units to integer
            except ValueError:
                raise serializers.ValidationError({"units": "Units must be a valid number."})
        
        return data
