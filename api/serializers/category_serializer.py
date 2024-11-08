from rest_framework import serializers
from api.models.category_model import Category

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name',)
        read_only_fields = ('id',)  # Make id read-only
