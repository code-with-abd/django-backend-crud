import traceback
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from api.serializers.item_serializers import ItemSerializer
from ..utils import validate_integer
from api.models.items_model import Item
from api.models.pagination_class import CustomPagination
from rest_framework.exceptions import NotFound

@api_view(['GET'])
def ApiOverview(request):
    api_urls = {
        'All items': '/items/',
        'Update': '/update_item/{id}',
        'Delete Item': '/delete_item/{id}',
        'Add': '/create_item/'
    }
 
    return Response(api_urls)

# ------------------Items----------------------------#

@api_view(['GET'])
def items(request):
    try:    
        name = request.query_params.get('name', "").strip()
        category = request.query_params.get('category', "").strip()

        # Start with all items
        items = Item.objects.all()

        # Apply filters only if parameters are provided
        if name:
            items = items.filter(name__icontains=name)
        if category:
            # By ID of category
            # items = items.filter(category=categoryID)
            # By name
            items = items.filter(category__name__icontains=category)  # Filter by category name

        # # Serialize the filtered items
        # serializer = ItemSerializer(items, many=True)
        # # Return the serialized data
        # return Response(data={'data': serializer.data}, status=status.HTTP_200_OK)

        # Apply pagination
        paginator = CustomPagination()
        try:
            paginated_items = paginator.paginate_queryset(items, request)
        except NotFound:
            # If an invalid page is requested, return an appropriate message
            return Response({
                'error': 'Invalid page number requested.',
            }, status=status.HTTP_404_NOT_FOUND)

        # Serialize paginated items
        serializer = ItemSerializer(paginated_items, many=True)

        # Return paginated response with serialized data
        return paginator.get_paginated_response(serializer.data)
    
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
def add_items(request):
    amount =  validate_integer(request.data.get('amount'), 'amount')
    units =  validate_integer(request.data.get('units'), 'units')
    data = {
        'category': request.data.get('category'),
        'name': request.data.get('name'),
        'amount': amount,
        'units': units,
        'picture': request.FILES.get('picture'),
        'createdBy': request.data.get('createdBy'), 
    }
    
    
    # Check if a item with this name already exists
    if Item.objects.filter(name=data['name']).exists():
        return Response({
            'error': 'Already added'
        }, status=status.HTTP_400_BAD_REQUEST)

    serializer = ItemSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
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

@api_view(['DELETE'])
def delete_item(request, id):
    # Retrieve the item or return a 404 if not found
    item = get_object_or_404(Item, id=id)
    item.delete()    
    return Response(data={'success': True, 'message': 'Deleted Successfully'}, status=status.HTTP_200_OK)
