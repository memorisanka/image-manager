from rest_framework import serializers

from .models import Image


class ImageSerializer(serializers.ModelSerializer):
    thumbnail_200 = serializers.ImageField(read_only=True)
    thumbnail_400 = serializers.ImageField(read_only=True)
    original_link = serializers.URLField(read_only=True)
    expiration_seconds = serializers.IntegerField(read_only=True)

    @staticmethod
    def validate_image(value):
        image_extension = value.name.split('.')[-1]
        if image_extension not in ['jpg', 'jpeg', 'png']:
            raise serializers.ValidationError('Invalid image format. Please upload a JPG or PNG file.')
        return value

    def create(self, validated_data):
        image = validated_data['image']
        # Process the image here
        return image

    class Meta:
        model = Image
        fields = ['id', 'owner', 'image', 'thumbnail_200', 'thumbnail_400', 'original_link', 'expiration_seconds']
        read_only_fields = ['owner', 'thumbnail_200', 'thumbnail_400', 'original_link', 'expiration_seconds']
