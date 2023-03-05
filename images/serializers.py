from rest_framework import serializers

from .models import Image


class ImageSerializer(serializers.ModelSerializer):

    @staticmethod
    def validate_image(value):
        image_extension = value.name.split('.')[-1]
        if image_extension not in ['jpg', 'jpeg', 'png']:
            raise serializers.ValidationError('Invalid image format. Please upload a JPG or PNG file.')
        return value


    class Meta:
        model = Image
        fields = ('id', 'owner', 'original_image',)
