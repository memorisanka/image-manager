from PIL import Image
from django.contrib.auth.models import AbstractUser, User
from django.contrib.auth.models import AbstractUser, User
from django.db import models


class Profile(models.Model):
    BASIC = 'basic'
    PREMIUM = 'premium'
    ENTERPRISE = 'enterprise'

    PLAN_CHOICES = [
        (BASIC, 'Basic'),
        (PREMIUM, 'Premium'),
        (ENTERPRISE, 'Enterprise'),
    ]

    parent_name = models.OneToOneField(User, on_delete=models.CASCADE)
    plan = models.CharField(max_length=20, choices=PLAN_CHOICES, default=BASIC)

    def __str__(self):
        return self.parent_name.username


class MyImage(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    original_image = models.ImageField(upload_to=f"img/")
    thumbnail_200 = models.ImageField(upload_to=f"img/thumb_200/", null=True, blank=True)
    thumbnail_400 = models.ImageField(upload_to=f"img/thumb_400/", null=True, blank=True)