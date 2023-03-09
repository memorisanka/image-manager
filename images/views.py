from io import BytesIO

from PIL import Image as PilImage
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.views import View
from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from .models import MyImage
from .serializers import MyImageSerializer


# View to list all images or create a new image
class ImageList(generics.ListCreateAPIView):
    queryset = MyImage.objects.all()
    serializer_class = MyImageSerializer
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
    @staticmethod
    def get(request, *args, **kwargs):
        image_id = kwargs['image_id']
        image = MyImage.objects.get(id=image_id)

        with BytesIO(image.original_image.read()) as file:
            with PilImage.open(file) as image:
                thumbnail = image.resize((300, 300))
                buffer = BytesIO()
                thumbnail.save(buffer, format='PNG')

        return HttpResponse(buffer.getvalue(), content_type='image/png')


# View to retrieve, update, or delete an image
class ImageDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = MyImage.objects.all()
    serializer_class = MyImageSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_update(self, serializer):
        # set owner of the image to current user
        serializer.save(owner=self.request.user)


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
        image = MyImage.objects.get(pk=image_id, owner=request.user)
    except MyImage.DoesNotExist:
        return Response({'error': 'Image not found'}, status=status.HTTP_404_NOT_FOUND)
    expiring_link = image.generate_expiring_link(expiration_time)
    return Response({'expiring_link': expiring_link}, status=status.HTTP_200_OK)
