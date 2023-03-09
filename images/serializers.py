from io import BytesIO

from PIL import Image as PilImage
from django.core.files.base import ContentFile
from rest_framework import serializers

from .models import MyImage


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
                self.thumbnail_200.save(self.original_image.name, ContentFile(buffer.getvalue()), save=False)
            elif max_height == 400:
                self.thumbnail_400.save(self.original_image.name, ContentFile(buffer.getvalue()), save=False)
            else:
                raise ValueError('Invalid max height')


class MyImageSerializer(serializers.ModelSerializer):

    @staticmethod
    def validate_image(value):
        image_extension = value.name.split('.')[-1]
        if image_extension not in ['jpg', 'jpeg', 'png']:
            raise serializers.ValidationError('Invalid image format. Please upload a JPG or PNG file.')
        return value

    class Meta:
        model = MyImage
        fields = ['id', 'owner', 'original_image']
