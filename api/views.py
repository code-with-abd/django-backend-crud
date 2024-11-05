import traceback
from django.shortcuts import get_object_or_404
from rest_framework.permissions import AllowAny
from rest_framework.decorators import permission_classes, api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, logout
from .utils import validate_integer
from api.models import Item, Category
from api.serializers import CategorySerializer, ItemSerializer, UserSerializer

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
             # Retrieve all items
        items = Item.objects.all().filter(name__icontains = name)
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

# ------------------User Session----------------------------#

@api_view(['POST'])
@permission_classes([AllowAny])  # Allow access without authentication
def sign_in(request):
    # Get the username and password from the request data
    username = request.data.get('username')
    password = request.data.get('password')
    
    # Authenticate the user
    user = authenticate(request, username=username, password=password)
    
    if user:
        # User is authenticated, get or create a token for the user
        token, _ = Token.objects.get_or_create(user=user)
        
        return Response({
            'token': token.key,
            'username': user.username,
            'id': user.id,
            'message': 'Sign-in successful!'
        }, status=status.HTTP_200_OK)
    else:
        # Invalid credentials
        return Response({
            'error': 'Invalid username or password'
        }, status=status.HTTP_401_UNAUTHORIZED)
    


@api_view(['POST'])
def log_out(request):
    # Get the user's token and delete it
    try:
        token = Token.objects.get(user=request.user)
        token.delete()  # Delete the token to invalidate future requests
    except Token.DoesNotExist:
        # If the token does not exist, skip deletion
        pass

    # Log out the user to clear session data
    logout(request)

    # Return a success response
    return Response(
        {'message': 'Successfully logged out.'},
        status=status.HTTP_200_OK
    )
    
@api_view(['POST'])
@permission_classes([AllowAny])
def sign_up(request):
    serializer = UserSerializer(data=request.data)
    
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# ------------------Categories----------------------------#

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