from rest_framework import serializers
from .models import Profile
from django.contrib.auth import get_user_model

User = get_user_model()

class CustomUserSerializer(serializers.ModelSerializer):
    '''
    This serializer handles user creation and validation of passwords.
    It includes fields for username, email, password, and password confirmation (password2).
    '''
    email = serializers.EmailField(write_only=True, allow_blank=True)
    password = serializers.CharField(write_only=True, required=True)
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'password2']
        extra_kwargs = {
            'email': {'required': False},  # Make email optional
        }

    def validate(self, data):
        '''
        Custom validation to ensure that:
        - Username is unique.
        - Password and password confirmation match.
        
        Raises:
            serializers.ValidationError: If the username already exists or if passwords do not match
        '''
        if User.objects.filter(username=data['username']).exists():
            raise serializers.ValidationError({'username': "A user with this username already exists!"})
        
        if data['password'] != data['password2']:
            raise serializers.ValidationError({'password': "Password fields do not match."})
        return data
    
    def create(self, validated_data):
        user = User.objects.create_user(
            username = validated_data['username'],
            email = validated_data['email'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
    
class ProfileSerializer(serializers.ModelSerializer):
    '''
    serializer to update user profile
    '''
    class Meta:
        model = Profile
        fields = ['age', 'weight']