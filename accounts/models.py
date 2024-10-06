from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model

class CustomUser(AbstractUser):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(max_length=250, blank=True, null=True)
    password = models.CharField(max_length=120)

User = get_user_model()

class Profile(models.Model):
    '''
    Represents personal details of the user, which can be used for measuring 
    calories burned during activities. Each user can have one associated profile.
    '''
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    age = models.PositiveIntegerField(null=True)
    weight = models.FloatField(null=True)