from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Profile, MyImage


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()


@receiver(post_save, sender=MyImage)
def create_thumbnails(sender, instance, created, **kwargs):
    if created:
        instance.create_thumbnail(max_height=200)
        instance.create_thumbnail(max_height=400)
