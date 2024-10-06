from rest_framework import serializers
from .models import Workout

class WorkoutSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workout
        fields = [
            'activity_type',
            'start_time',
            'end_time',
            'duration',
            'distance',
            'calories_burned', 
            'date']
        read_only_fields = ['duration', 'calories_burned', 'end_time'] # No manual edits can be done during creates & updates

        def validate(self, data):
            if data['activity_type'] is None:
                raise serializers.ValidationError({'message': "activity type is needed for every workout!"})
            return data
        
class WorkoutListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workout
        fields = [
            'id',
            'activity_type',
            'duration',
            'distance', 
            'calories_burned', 
            'date']