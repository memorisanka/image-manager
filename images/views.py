from io import BytesIO

from PIL import Image as PilImage
from django.core.exceptions import PermissionDenied
from django.views import View
from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from .models import Image
from .serializers import ImageSerializer


# View to list all images or create a new image
class ImageList(generics.ListCreateAPIView):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        # set owner of the image to current user

        serializer.save(owner=self.request.user)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class MyView(View):
    def get(self, request, *args, **kwargs):
        image_id = kwargs['image_id']
        image = Image.objects.get(id=image_id)
        # image_data = image.original_image.read()

        with BytesIO(image.original_image.read()) as file:
            with PilImage.open(file) as image:
                thumbnail = image.resize((300, 300))
                buffer = BytesIO()
                thumbnail.save(buffer, format='PNG')


"""
zamiast
"original_image": "http://localhost:8000/images/AameoGKqdQYN_9299_700.jpeg"

"original_image": "http://localhost:8000/img/<ID>"

"thumb_200": "http://localhost:8000/img/<ID>/thumb_200"

path('img/<int:image_id>/', MyView.as_view()),

class MyView(View):
    def get(self, request, *args, **kwargs):
        image_id = kwargs['image_id']
        image = Image.objects.get(id=image_id)
        # image_data = image.original_image.read()

        with BytesIO(image.original_image.read()) as file:
            with PilImage.open(file) as image:
                thumbnail = image.resize((300, 300))
                buffer = BytesIO()
                thumbnail.save(buffer, format='PNG')
"""


# View to retrieve, update, or delete an image
class ImageDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_update(self, serializer):
        # set owner of the image to current user
        serializer.save(owner=self.request.user)


#
# # View to handle image uploads
# @api_view(['POST'])
# @permission_classes([permissions.IsAuthenticated])
# @csrf_exempt
# def image_upload(request):
#     # check if the user has the necessary plan for uploading images
#     if request.user.profile.plan == 'Basic':
#         max_thumbnail_height = 200
#     elif request.user.profile.plan == 'Premium' or request.user.profile.plan == 'Enterprise':
#         max_thumbnail_height = 400
#     else:
#         raise PermissionDenied
#
#     # parse file upload from request data
#     parser_classes = (FileUploadParser,)
#     file = request.data['file']
#     filename = file.name
#     image = Image(owner=request.user, original_image=file)
#
#     # create thumbnails and set image urls
#     image.create_thumbnail(max_thumbnail_height)
#     if request.user.profile.plan == 'Premium' or request.user.profile.plan == 'Enterprise':
#         thumb = image.create_thumbnail(200)
#         image_url = request.build_absolute_uri(image.original_image.url)
#     else:
#         image_url = None
#     image.save()
#
#     # serialize image and return response
#     serializer = ImageSerializer(image)
#     return Response(serializer.data, status=status.HTTP_201_CREATED)


# View to handle expiring image links
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def image_link(request):
    # check if the user has the necessary plan for generating expiring links
    if request.user.profile.plan != 'Enterprise':
        raise PermissionDenied

    # parse expiration time from request data
    expiration_time = request.data.get('expiration_time')
    if expiration_time is None or not (300 <= expiration_time <= 30000):
        return Response({'error': 'Invalid expiration time'}, status=status.HTTP_400_BAD_REQUEST)

    # generate expiring link and return response
    image_id = request.data.get('image_id')
    try:
        image = Image.objects.get(pk=image_id, owner=request.user)
    except Image.DoesNotExist:
        return Response({'error': 'Image not found'}, status=status.HTTP_404_NOT_FOUND)
    expiring_link = image.generate_expiring_link(expiration_time)
    return Response({'expiring_link': expiring_link}, status=status.HTTP_200_OK)
