import traceback
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from api import serializers
from api.models import Item
from api.serializers import ItemSerializer

@api_view(['GET'])
def ApiOverview(request):
    api_urls = {
        'all_users': '/users',
        'all_items': '/items',
        'Search by Category': '/?category=category_name',
        'Search by Subcategory': '/?subcategory=category_name',
        'Add': '/create',
        'Update': '/update/pk',
        'Delete': '/item/pk/delete'
    }
 
    return Response(api_urls)

@api_view(['POST'])
def add_items(request):
    try:
        item = ItemSerializer(data=request.data)
        
        # Check if the item already exists
        if Item.objects.filter(**request.data).exists():
            return Response(data={'message': 'Item already exists'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Validate and save the item if it’s valid
        if item.is_valid():
            item.save()
            return Response(item.data, status=status.HTTP_201_CREATED)
        
        # Return validation errors if the item is not valid
        return Response(item.errors, status=status.HTTP_400_BAD_REQUEST)
    
    except Exception as e:
        # Log the error with traceback for debugging
        error_trace = traceback.format_exc()
        print(error_trace)  # Or log it using Django’s logging framework
        
        # Respond with the error details
        return Response(
            data={'error': str(e), 'trace': error_trace},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    
@api_view(['PUT'])
def update_item(request, id):
    # Retrieve the item or return a 404 if not found
    item = get_object_or_404(Item, id=id)
    
    # Deserialize and validate incoming data (partial=True allows for partial updates)
    serializer = ItemSerializer(item, data=request.data, partial=True)
    
    if serializer.is_valid():
        serializer.save()  # Save updates to the database
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)