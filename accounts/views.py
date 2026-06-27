from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import UserProfileSerializer

from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status

# This dynamically fetches whatever model is specified in your AUTH_USER_MODEL settings
User = get_user_model()

@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(view_request):
    data = view_request.data
    
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')
    account_type = data.get('account_type', 'regular')
    fips_codes = data.get('fips_codes', []) 

    if not username or not password or not email:
        return Response(
            {"error": "Username, password, and email are required fields."}, 
            status=status.HTTP_400_BAD_REQUEST
        )

    # This will now safely check against your CustomUser table!
    if User.objects.filter(username=username).exists():
        return Response(
            {"error": "A user with that username already exists."}, 
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        # Create your CustomUser object directly
        user = User.objects.create(
            username=username,
            email=email,
            password=make_password(password),
            account_type=account_type,
            fips_codes=fips_codes
        )
        
        return Response(
            {"message": f"Account successfully created for {username}!"}, 
            status=status.HTTP_201_CREATED
        )
        
    except Exception as e:
        return Response(
            {"error": f"Something went wrong: {str(e)}"}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

class UserProfileView(APIView):
    # Protect this endpoint! Users MUST be logged in to access this data
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # 'request.user' automatically grabs whoever is currently logged in
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data)
    
@api_view(['POST'])
@permission_classes([AllowAny]) # Anyone can access the sign-up page
def register_user(view_request):
    data = view_request.data
    
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')
    account_type = data.get('account_type', 'regular')
    fips_codes = data.get('fips_codes', []) # Expecting an array/list

    # 1. Basic validation
    if not username or not password or not email:
        return Response(
            {"error": "Username, password, and email are required fields."}, 
            status=status.HTTP_400_BAD_REQUEST
        )

    if User.objects.filter(username=username).exists():
        return Response(
            {"error": "A user with that username already exists."}, 
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        # 2. Create the core Django User safely (this automatically hashes the password)
        user = User.objects.create(
            username=username,
            email=email,
            password=make_password(password)
        )
        
        # 3. Save your custom metadata fields (Account Type & FIPS list)
        # If you have a UserProfile model set up:
        # UserProfile.objects.create(user=user, account_type=account_type, fips_codes=fips_codes)
        
        return Response(
            {"message": f"Account successfully created for {username}!"}, 
            status=status.HTTP_201_CREATED
        )
        
    except Exception as e:
        return Response(
            {"error": f"Something went wrong: {str(e)}"}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )