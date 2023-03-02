from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User
from images.models import Image
from rest_framework import permissions


class FileUploadView(APIView):
    parser_classes = [FileUploadParser]
    queryset = User.objects.all()
    permission_classes = []
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, filename, format=None):
        user = request.user  # User
        file_obj = request.data['file']
        obj = Image(user_profile=user.profile, image=file_obj)
        obj.save()
        print("TEST", file_obj, type(file_obj))
        return Response(status=204)

"""
Custom user mode:
https://docs.djangoproject.com/en/4.1/topics/auth/customizing/

przykład:
https://github.com/bkwi/pywars/blob/develop/users/models.py


class User:
  username = ...

class Profile:
  user = ...

class Image(models.Model):
  user_profile = ForeignKey(Profile, related_name='images')
  image = ImageField()
  
  
user.profile.images



"""