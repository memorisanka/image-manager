from rest_framework import viewsets, permissions, generics, status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Image
from .serializers import ImageSerializer


class ImageList(viewsets.ViewSet):
    def list(self, request):
        queryset = Image.objects.all()
        serializer = ImageSerializer(queryset, many=True)
        return Response(serializer.data)


class ImageUploadView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = ImageSerializer(data=request.data)

        if serializer.is_valid():
            image = serializer.save(owner=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ImageView(generics.RetrieveAPIView):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return get_object_or_404(Image, id=self.kwargs['image_id'], owner=self.request.user.id)


class ThumbnailView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, image_id, size):
        image = get_object_or_404(Image, id=image_id, owner=request.user.id)
        thumbnail = image.generate_thumbnail(size)
        return Response({'thumbnail_url': thumbnail.url})


class ExpireLinkView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, image_id):
        image = get_object_or_404(Image, id=image_id, owner=request.user.id)
        expire_seconds = int(request.data.get('expire_seconds', 300))
        link = image.generate_expiring_link(expire_seconds)
        return Response({'link': link.url})

#
# @api_view(['POST'])
# @permission_classes([permissions.IsAuthenticated])
# def image_upload(request):
#     serializer = ImageSerializer(data=request.data)
#     if serializer.is_valid():
#         image = serializer.validated_data['image']
#         owner = request.user
#         image_obj = Image.objects.create(owner=owner, image=image)
#         if owner.plan == User.BASIC:
#             thumbnail_path = generate_thumbnail(image_obj.image.path, 200)
#             image_obj.thumbnail_200 = thumbnail_path
#             image_obj.save()
#         elif owner.plan == User.PREMIUM:
#             thumbnail_path_200 = generate_thumbnail(image_obj.image.path, 200)
#             thumbnail_path_400 = generate_thumbnail(image_obj.image.path, 400)
#             image_obj.thumbnail_200 = thumbnail_path_200
#             image_obj.thumbnail_400 = thumbnail_path_400
#             image_obj.original_link = image_obj.image.url
#             image_obj.save()
#         elif owner.plan == User.ENTERPRISE:
#             thumbnail_path_200 = generate_thumbnail(image_obj.image.path, 200)
#             thumbnail_path_400 = generate_thumbnail(image_obj.image.path, 400)
#             image_obj.thumbnail_200 = thumbnail_path_200
#             image_obj.thumbnail_400 = thumbnail_path_400
#             image_obj.original_link = image_obj.image.url
#             image_obj.expiration_seconds = None
#             image_obj.save()
#         return Response(ImageSerializer(image_obj).data, status=status.HTTP_201_CREATED)
#     return Response

# """
# Custom user mode:
# https://docs.djangoproject.com/en/4.1/topics/auth/customizing/
#
# przykład:
# https://github.com/bkwi/pywars/blob/develop/users/models.py
#
#
# class User:
#   username = ...
#
# class Profile:
#   user = ...
#
# class Image(models.Model):
#   user_profile = ForeignKey(Profile, related_name='images')
#   image = ImageField()
#
#
# user.profile.images
#
#
#
# """


# class ImageListCreateView(generics.ListCreateAPIView):
#     serializer_class = ImageSerializer
#     permission_classes = [permissions.IsAuthenticated]
#
#     def get_queryset(self):
#         user = self.request.user
#         return Image.objects.filter(user=user)
#
#     def perform_create(self, serializer):
#         image_url = self.request.data.get('image_url')
#
#         # Download the image from the URL
#         response = requests.get(image_url)
#         content_type = response.headers.get('content-type')
#         if 'image/jpeg' not in content_type and 'image/png' not in content_type:
#             return Response({'error': 'Invalid image format. Only JPEG and PNG are supported.'},
#                             status=status.HTTP_400_BAD_REQUEST)
#         file_name = image_url.split('/')[-1]
#         file_content = ContentFile(response.content)
#         serializer.validated_data['image'] = file_content
#         serializer.save(user=self.request.user)
#
#         # Create the thumbnails
#         instance = serializer.instance
#         instance.thumbnails.all().delete()
#         instance.thumbnails.all().save()
#
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
#

# import os
#
# import requests
# from rest_framework import status, permissions
# from rest_framework.response import Response
# from rest_framework.views import APIView
#
# from images.models import Image
# from images.serializers import ImageSerializer
#
#
# class ImageUploadView(APIView):
#     serializer_class = ImageSerializer
#     queryset = Image.objects.all()
#     permission_classes = [permissions.IsAuthenticatedOrReadOnly]
#
#     def post(self, request, filename):
#         serializer = self.serializer_class(data=request.data)
#         serializer.is_valid(raise_exception=True)
#
#         image_url = serializer.validated_data['image_url']
#
#         response = requests.get(image_url)
#
#         image_file = os.path.join('/media', 'image.jpg')
#         with open(image_file, 'wb') as f:
#             f.write(response.content)
#
#         return Response({'message': 'Image uploaded successfully'}, status=status.HTTP_201_CREATED)
#
#
