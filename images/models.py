from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator


class User(AbstractUser):
    BASIC = 'basic'
    PREMIUM = 'premium'
    ENTERPRISE = 'enterprise'

    PLAN_CHOICES = [
        (BASIC, 'Basic'),
        (PREMIUM, 'Premium'),
        (ENTERPRISE, 'Enterprise'),
    ]

    plan = models.CharField(max_length=20, choices=PLAN_CHOICES, default=BASIC)


class Image(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='images/')
    thumbnail_200 = models.ImageField(upload_to='images/thumbnails/200/', null=True, blank=True)
    thumbnail_400 = models.ImageField(upload_to='images/thumbnails/400/', null=True, blank=True)
    original_link = models.URLField(null=True, blank=True)
    expiration_seconds = models.PositiveIntegerField(validators=[MinValueValidator(300), MaxValueValidator(30000)], null=True, blank=True)

    def __str__(self):
        return self.image.name
