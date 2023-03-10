from io import BytesIO

from PIL import Image as PilImage
from django.contrib.auth.models import AbstractUser, User
from django.contrib.auth.models import AbstractUser, User
from django.core.files.base import ContentFile
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
    original_image = models.ImageField(upload_to="img/")
    thumbnail_200 = models.ImageField(upload_to=f"img/thumb_200/", null=True, blank=True)
    thumbnail_400 = models.ImageField(upload_to=f"img/thumb_400/", null=True, blank=True)

    def create_thumbnail(self, max_height):
        with BytesIO(self.original_image.read()) as file:
            with PilImage.open(file) as image:
                # calculate new width and height
                width, height = image.size
                ratio = max_height / height
                new_width = round(width * ratio)
                new_height = max_height
                # create thumbnail
                thumbnail = image.resize((new_width, new_height))
                # save thumbnail to buffer
                buffer = BytesIO()
                thumbnail.save(buffer, format='PNG')
                # save buffer to image field
                if max_height == 200:
                    self.thumbnail_200.save(self.thumbnail_200, ContentFile(buffer.getvalue()), save=False)
                elif max_height == 400:
                    self.thumbnail_400.save(self.thumbnail_400, ContentFile(buffer.getvalue()), save=False)
                else:
                    raise ValueError('Invalid max height')
