from django.urls import path
from . import views

urlpatterns = [
    path('workouts/new/', views.WorkoutCreateView.as_view(), name='workout-list-create'),
    path('workouts/', views.WorkoutListView.as_view(), name='workout-list'),
    path('workouts/<int:pk>/', views.WorkoutDetailView.as_view(), name='workout-detail'),
    path('workouts/<int:pk>/edit/', views.WorkoutUpdateView.as_view(), name='workout-update'),
    path('workouts/<int:pk>/delete/', views.WorkoutDeleteView.as_view(), name='workout-delete'),
    path('workouts/metrics/', views.WorkoutMetricsView.as_view(), name='workout-metrics'),
]