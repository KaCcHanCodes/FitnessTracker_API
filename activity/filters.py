import django_filters
from .models import Workout
# Filterset class to filter by date range, duration, and activity type
class WorkoutFilter(django_filters.FilterSet):
    date_range = django_filters.DateFromToRangeFilter(field_name='date')

    class Meta:
        model = Workout
        fields = ['activity_type', 'duration', 'date_range']