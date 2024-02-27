"""User profile app models."""

from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from users.models import CustomUser


class UserProfile(models.Model):
    """UserProfile model class."""

    class Gender(models.IntegerChoices):
        """Gender choice class."""

        NONE = 0
        FEMALE = 1
        MALE = 2
        OTHER = 3

    custom_user = models.OneToOneField("users.CustomUser", on_delete=models.CASCADE)
    gender = models.IntegerField(choices=Gender.choices, default=Gender.NONE)
    age = models.IntegerField(default=21)
    picture = models.ImageField(upload_to="profile_pictures/", blank=True)


@receiver(post_save, sender=CustomUser)
def create_profile(sender, instance, created, **kwargs):
    """Create an object of UserProfile when a user CustomUser object is created."""
    if sender and created:
        UserProfile.objects.create(custom_user=instance)


post_save.connect(create_profile, sender=CustomUser)
