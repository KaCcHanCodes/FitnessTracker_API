from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth import get_user_model
from django.utils.dateparse import parse_date
from django.utils import timezone
from django.db.models import Sum
from .filters import WorkoutFilter
from .utils import seconds_to_HHMMSS
from .models import Workout
from .serializers import WorkoutSerializer, WorkoutListSerializer
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError

User = get_user_model()

class WorkoutCreateView(generics.CreateAPIView):
    '''
    API endpoint that allows authenticated users to create a new workout.
    Permissions:
    - Authenticated users only.
    Description:
    - This view allows users to create a workout instance. The user_id is automatically
      retrieved from the authenticated user making the request and set in the workout instance.
    Methods:
    - POST: Create a new workout.
      - Requires the necessary workout fields in the request body.
      - Automatically assigns the user making the request as the `user_id` for the workout.
    '''
    serializer_class = WorkoutSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data) 
        if serializer.is_valid():
            serializer.save(user_id=self.request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class WorkoutListView(generics.ListAPIView):
    """
    List all workouts with optional filtering by activity type, workout name and date range.

    filterset_fields:
    - activity_type: Filter workouts by a specific activity type (e.g., 'running', 'cycling').
    - workout_name: Filter workouts by workout names
    - date: Filter workouts by date ranges

    Permissions:
    - Only authenticated users can access this view.
    """
    serializer_class = WorkoutListSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = WorkoutFilter #correction: Set filterset_fields to filter_class

    #override get_query to list workouts filtered by the request.user
    def get_queryset(self):
        return Workout.objects.filter(user_id=self.request.user)

class WorkoutDetailView(generics.RetrieveAPIView):
    '''
    This view allows authenticated users to access their workout details. 
    It supports retrieving a specific workout instance by its ID.

    Attributes:
        serializer_class: The serializer used for returning workout data.
        permission_classes: Permissions required to access this view.
    '''
    serializer_class = WorkoutListSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    #override get_query to list workouts filtered by the request.user
    def get_queryset(self):
        return Workout.objects.filter(user_id=self.request.user)

class WorkoutUpdateView(generics.RetrieveUpdateAPIView):
    '''
    - Allows users to retrieve and update details of a specific workout instance.
    - Authenticated users only.
    - Update method overridden, sets the end_location, calories_burned, and end_time attributes automatically.
    '''
    serializer_class = WorkoutSerializer
    permission_classes = [permissions.IsAuthenticated]

    # filter objects returned by the user_id
    def get_queryset(self):
        return Workout.objects.filter(user_id=self.request.user)

    def update(self, request, *args, **kwargs):
        activity = self.get_object() #get the instance model
        activity.activity_type = request.data.get('activity_type') # update activity type
        activity.end_time = timezone.now()  # get the current time
        activity.calories_burned = activity.calculate_calories() # run calculations on calories burned after each update to workout.
        serializer = WorkoutSerializer(activity, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

class WorkoutDeleteView(generics.DestroyAPIView):
    '''
    - Requires authentication (user must be logged in).
    - Only the authenticated user can delete their own workout.
    - If the workout does not belong to the user, the request will return a 403 Forbidden error.

    This endpoint deletes a single workout instance for the user.
    '''
    permission_classes = [permissions.IsAuthenticated]
    queryset = Workout.objects.all()

    def get_queryset(self):
        return Workout.objects.filter(user_id=self.request.user)

class WorkoutMetricsView(generics.ListAPIView):
    '''
    Function:
    View summary of all activities (total duration, total distance covered, and total caloried burned)
    over a given period.

    Query Parameters:
    - start_date (str): Start date of the range in "YYYY-MM-DD" format.
    - end_date (str): End date of the range in "YYYY-MM-DD" format.

    Responses:
    - 200 OK: Returns total duration, distance, and calories burned for the given period.
    - 400 Bad Request: If the date range is invalid or there are pending workouts (missing duration).
    
    Permissions:
    - Requires authenticated users to access.
    '''
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = WorkoutListSerializer

    def get(self, request, *args, **kwargs):
        #get date range from query parameters
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')

        #validate data inputs
        if start_date:
            start_date = parse_date(start_date)
            if not start_date:
                raise ValidationError({'start_date': "Invalid start date format"})
        if end_date:
            end_date = parse_date(end_date)
            if not end_date:
                raise ValidationError({'end_date': "Invalid start date format"})

        # filter workouts by the user within the date range
        workouts = Workout.objects.filter(user_id=request.user, date__range=(start_date, end_date))

        if workouts.filter(duration__isnull=True).exists():
            return Response({"error": "Please update all pending workouts before running metrics"}, status=status.HTTP_400_BAD_REQUEST)   
        #calculate metrics
        else:
            total_duration = workouts.aggregate(total_duration=Sum('duration'))['total_duration']
            total_distance = workouts.aggregate(total_distance=Sum('distance'))['total_distance']
            total_calories_burned = workouts.aggregate(total_calories_burned=Sum('calories_burned'))['total_calories_burned']

            if total_duration:
                #covert total duration from timedelta to seconds
                seconds = total_duration.total_seconds()
                #convert seconds to HH:MM:SS format
                readable_time_format = seconds_to_HHMMSS(seconds)
            else:
                readable_time_format = "00:00:00"

            response = {
                "start_date": start_date,
                "end_date": end_date,
                "total_duration": readable_time_format,
                "total_distance": total_distance,
                "total_calories_burned": total_calories_burned,
            }
            return Response(response, status=status.HTTP_200_OK)