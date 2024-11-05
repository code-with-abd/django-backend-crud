from rest_framework import serializers
from .models import Item, Category

from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'password')
        extra_kwargs = {'password': {'write_only': True}}  # Ensure the password is write-only

    def create(self, validated_data):
        # Ensure first_name is not empty
        if not validated_data.get('first_name'):
            raise serializers.ValidationError({'first_name': 'This field is required.'})

        # Ensure username is not empty
        if not validated_data.get('username'):
            raise serializers.ValidationError({'username': 'This field is required.'})

        # Create the user
        user = User(**validated_data)
        user.set_password(validated_data['password'])  # Hash the password
        user.save()
        return user 

      
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name',)
        read_only_fields = ('id',)  # Make id read-only

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
