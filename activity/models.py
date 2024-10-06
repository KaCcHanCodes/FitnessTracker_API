from django.contrib.gis.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Workout(models.Model):
    '''
    Model representing workout information based on activity type.
    
    Fields:
    - user_id: Foreign key linking the workout to a user.
    - activity_type: The type of workout activity (e.g., Walking, Running).
    - start_time: The timestamp when the workout started (automatically set when the workout is created).
    - end_time: The timestamp when the workout ended.
    - duration: The total duration of the workout (calculated based on start_time and end_time).
    - distance: The distance covered during the workout (optional, for activities like running or cycling).
    - calories_burned: The total calories burned during the workout (calculated based on MET values).
    - date: The date when the workout was created (automatically set when the workout is created).
    
    Methods:
    - calculate_calories: Calculates calories burned based on the user's weight, the workout duration, 
                          and the activity's MET value.
    '''
    ACTIVITY_TYPE = [
        ('Walking', "Walking at moderate speed (4 km/h)"),
        ('Skipping', "Jumping rope, light workout"),
        ('Running', "Running at 9.6 km/h"),
        ('Cycling', "Cycling at a moderate pace"),
        ('Weightlifting', "Light/moderate effort Weight Training"),
    ]
    
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activity')
    activity_type = models.CharField(max_length=50, choices=ACTIVITY_TYPE)
    start_time = models.DateTimeField(auto_now_add=True, null=True)
    end_time = models.DateTimeField(null=True, blank=True)
    duration = models.DurationField(null=True, blank=True) #duration of activity
    distance = models.FloatField(null=True, blank=True) #distance in meters                (refactor later)
    calories_burned = models.FloatField(null=True, blank=True) #calories burned
    date = models.DateTimeField(auto_now_add=True)
        
    def calculate_calories(self):
        '''
        Calculates the number of calories burned during the workout based on MET values,
        user's weight, and workout duration.
        Returns:
        - calories_burned: Type Float, the estimated calories burned during the workout.
        '''
        # fetch weight data from user profile
        weight = self.user_id.profile.weight
        if weight is None:
            weight = 1 #default value for weight

        duration_in_seconds = (self.end_time - self.start_time).total_seconds() #calculate duration and convert to seconds

        #set default MET values for activity types
        MET_VALUES = {
            "Walking": 3.0,
            "Skipping": 10.0,
            "Running": 9.8,
            "Cycling": 6.0,
            "Weightlifting": 4.7,
        }

        met_value = MET_VALUES.get(self.activity_type, 1.0) #get MET values, else default MET value is 1.0
        duration = duration_in_seconds / 60 #convert duration from seconds to minutes

        # Calculate calories burned using the MET formula
        calories_burned = met_value * 3.5 * weight * duration / 200
        return calories_burned  