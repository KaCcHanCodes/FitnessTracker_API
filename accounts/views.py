from rest_framework import generics, permissions, status
from rest_framework_simplejwt.authentication import JWTAuthentication
from .serializers import CustomUserSerializer, ProfileSerializer
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from .models import Profile


User = get_user_model()

class UserRegisterView(generics.CreateAPIView):
    '''
    This view allows a new user to register by creating a new user account.

    - POST: Create a new user account.

    Request Body Parameters:
    - `username` (string): The desired username for the user. It should be unique.
    - `email` (string): The user's email address. It should be unique.
    - `password` (string): The desired password for the user account.
    
    Response:
    - 201 Created: If the user registration is successful, it returns the user data.
    - 400 Bad Request: If the provided data is invalid, it returns an error message.

    This view uses the `CustomUserSerializer` to validate the request data and create the user account.
    '''
    serializer_class = CustomUserSerializer

    def post(self, request, *args, **kwargs):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserProfileView(generics.RetrieveUpdateAPIView):
    '''
    - Method: GET to retrieve the profile, PUT/PATCH to update the profile
    - Permissions: Only authenticated users can access this endpoint
    - Authentication: JWT Authentication is required
    - Response:
        - 200: Returns the user profile details upon a successful GET request
        - 201: Returns the updated profile details upon a successful PUT/PATCH request
        - 400: Returns validation errors in case of an invalid request
    '''
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    serializer_class = ProfileSerializer

    def get_queryset(self):
        return Profile.objects.filter(user=self.request.user)