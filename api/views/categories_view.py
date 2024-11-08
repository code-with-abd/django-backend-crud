import traceback
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from api.models.category_model import Category
from api.serializers.category_serializer import CategorySerializer

@api_view(['GET'])
def categories(request):
    try:
             # Retrieve all Category
        category = Category.objects.all()
        serializer = CategorySerializer(category, many=True)
        
        # Return the serialized data
        return Response(data={'data': serializer.data}, status=status.HTTP_200_OK)
    
    except Exception as e:
        # Log the error with traceback for debugging
        error_trace = traceback.format_exc()
        print(error_trace)  # Or log it using Django’s logging framework
        
        # Respond with the error details
        return Response(
            data={'error': str(e), 'trace': error_trace},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['POST'])
def add_category(request):
    # Extract the category name from the request data
    category_name = request.data.get('name')
    
    # Check if the category already exists
    if Category.objects.filter(name=category_name).exists():
        return Response(data={'message': 'Category already exists'}, status=status.HTTP_400_BAD_REQUEST)

    # Create a serializer instance with the new category data
    serializer = CategorySerializer(data={'name': category_name})
  
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def delete_category(request, id):
    # Retrieve the category or return a 404 if not found
    category = get_object_or_404(Category, id=id)
    category.delete()    
    return Response(data={'success': True, 'message': 'Deleted Successfully'}, status=status.HTTP_200_OK)