from rest_framework import serializers
from .models import Item

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

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ('id', 'category',  'name', 'amount', 'picture')
        read_only_fields = ('id',)  # Make id read-only
        def to_internal_value(self, data):
         data = super().to_internal_value(data)
         try:
            data['amount'] = int(data['amount'])  # Convert amount to integer
         except ValueError:
            raise serializers.ValidationError({"amount": "Amount must be a valid number."})
         return data