from rest_framework.permissions import AllowAny
from rest_framework.decorators import permission_classes, api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, logout
from ..serializers import user_serializer

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
    serializer = user_serializer.UserSerializer(data=request.data)
    
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
