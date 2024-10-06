from django.urls import path, re_path
from . import views

urlpatterns = [
    path('register/', views.UserRegisterView.as_view(), name='register'),
    path('profile/update/', views.UserProfileView.as_view(), name='profile-update'),
]