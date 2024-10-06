from .models import Workout
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.utils import timezone

@receiver(pre_save, sender=Workout)
def EndWorkout(sender, instance, **kwargs):
    if instance.end_time:
        instance.duration = instance.end_time - instance.start_time

    # if instance.start_location and instance.end_location:
    #     #calculate the distance in meters
    #     instance.distance = (instance.start_location - instance.end_location) * 1000