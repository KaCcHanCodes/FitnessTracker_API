from .models import Profile, CustomUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ObjectDoesNotExist

#signal to create user profile when a user is registered
@receiver(post_save, sender=CustomUser)
def CreateUserProfile(sender, instance, created, **kwargs):
    try:
        instance.profile.save()
    except ObjectDoesNotExist:
        Profile.objects.create(user=instance)

#signal to save user profile when user is updated
@receiver(post_save, sender=CustomUser)
def SaveUserProfile(sender, instance, **kwargs):
    instance.profile.save()