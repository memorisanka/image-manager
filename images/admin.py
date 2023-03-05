from django.contrib import admin

from images.models import Image, User

admin.site.register(User)
admin.site.register(Image)
