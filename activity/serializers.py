from rest_framework import serializers
from .models import Workout

class WorkoutSerializer(serializers.ModelSerializer):
    '''
    This serializer handles workout creation and validation of activity type.
    It includes all fields outlined in the workout model.
    Read only permission is enabled for duration, calories burned, and end time fields. 
    '''
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
            if self.context['request'].method == "POST" or self.context['request'].method == "PUT":
                if data['activity_type'] is None:
                    raise serializers.ValidationError({'message': "activity type is needed for every workout!"})
                return data
        
        def update(self, instance, validated_data):
            if self.context['request'].method == "PATCH":
                instance.distance = validated_data.get('distance', instance.distance)
                instance.activity_type = validated_data.get('activity_type', instance.activity_type)
                instance.save()
                return instance

class WorkoutListSerializer(serializers.ModelSerializer):
    '''
    This serializer is used to display a summary of workout entries in list and detail views. 
    It represents relevant details like the instance id, activity type, duration, distance covered, 
    calories burned, and the date of the workout.
    '''
    class Meta:
        model = Workout
        fields = [
            'id',
            'activity_type',
            'duration',
            'distance', 
            'calories_burned', 
            'date']