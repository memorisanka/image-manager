from django.core.exceptions import PermissionDenied
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.parsers import FileUploadParser
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


# View to retrieve, update, or delete an image
class ImageDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_update(self, serializer):
        # set owner of the image to current user
        serializer.save(owner=self.request.user)


# View to handle image uploads
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
@csrf_exempt
def image_upload(request):
    # check if the user has the necessary plan for uploading images
    if request.user.plan == 'Basic':
        max_thumbnail_height = 200
    elif request.user.plan == 'Premium' or request.user.plan == 'Enterprise':
        max_thumbnail_height = 400
    else:
        raise PermissionDenied

    # parse file upload from request data
    parser_classes = (FileUploadParser,)
    file = request.data['file']
    filename = file.name
    image = Image(owner=request.user, original_file=file)

    # create thumbnails and set image urls
    image.create_thumbnail(max_thumbnail_height)
    if request.user.plan == 'Premium' or request.user.plan == 'Enterprise':
        image.create_thumbnail(200)
        image_url = request.build_absolute_uri(image.original_file.url)
    else:
        image_url = None
    image.save()

    # serialize image and return response
    serializer = ImageSerializer(image)
    return Response(serializer.data, status=status.HTTP_201_CREATED)


# View to handle expiring image links
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def image_link(request):
    # check if the user has the necessary plan for generating expiring links
    if request.user.plan != 'Enterprise':
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
