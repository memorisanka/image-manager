"""image_manager URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from images.views import ImageUploadView, ImageView, ThumbnailView, ExpireLinkView, ImageList

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', ImageList.as_view({'get': 'list'}), name='image-list'),
    path('images/', ImageUploadView.as_view(), name='image-upload'),
    path('images/<int:image_id>/', ImageView.as_view(), name='image-detail'),
    path('images/<int:image_id>/thumbnail/<int:size>/', ThumbnailView.as_view(), name='image-thumbnail'),
    path('images/<int:image_id>/expire-link/', ExpireLinkView.as_view(), name='image-expire-link'),
]
