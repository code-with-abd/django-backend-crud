import traceback
from django.shortcuts import get_object_or_404
from rest_framework.permissions import AllowAny
from rest_framework.decorators import permission_classes, api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from api import serializers
from api.models import Item
from api.serializers import ItemSerializer, UserSerializer

@api_view(['GET'])
def ApiOverview(request):
    api_urls = {
        'All items': '/items/',
        'Update': '/update_item/{id}',
        'Delete Item': '/delete_item/{id}',
        'Add': '/create_item/'
    }
 
    return Response(api_urls)


@api_view(['GET'])
def items(request):
    try:
             # Retrieve all items
        items = Item.objects.all()

          # Get the 'name' query parameter from the request (if provided)
        # name_query = request.query_params.get('name', None)
        
        # # Filter items by name if a search term is provided
        # if name_query:
        #     items = Item.objects.filter(name__icontains=name_query)
        # else:
        #     items = Item.objects.all()
        
        # Serialize the items
        serializer = ItemSerializer(items, many=True)
        
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
    
@api_view(['DELETE'])
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

@api_view(['POST'])
@permission_classes([AllowAny])  # Allow access without authentication
def sign_in(request):
    # Get the username and password from the request data
    username = request.data.get('username')
    password = request.data.get('password')
    
    # Authenticate the user
    user = authenticate(request, username=username, password=password)
    
    if user is not None:
        # User is authenticated, get or create a token for the user
        token, created = Token.objects.get_or_create(user=user)
        
        return Response({
            'token': token.key,
            'username': user.username,
            'message': 'Sign-in successful!'
        }, status=status.HTTP_200_OK)
    else:
        # Invalid credentials
        return Response({
            'error': 'Invalid username or password'
        }, status=status.HTTP_401_UNAUTHORIZED)
    
@api_view(['POST'])
@permission_classes([AllowAny])
def sign_up(request):
    serializer = UserSerializer(data=request.data)
    
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)