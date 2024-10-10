from .models import Workout
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.utils import timezone

# This signal calculates the duration of a workout when it's updated
@receiver(pre_save, sender=Workout)
def EndWorkout(sender, instance, **kwargs):
    if instance.end_time:
        instance.duration = instance.end_time - instance.start_time