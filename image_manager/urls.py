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

from images import views
from images.views import ImageDetail, ImageList, MyView

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', ImageList.as_view(), name='image-list'),
    path('images/', views.image_upload, name='image-upload'),
    path(r'images/(?P<pk>\d+)/', ImageDetail.as_view(), name='image-detail'),
    path('img/<int:image_id>/', MyView.as_view()),
    path('images/<int:image_id>/expire-link/', views.image_link, name='image-expire-link'),
]

# (?P<pk>\d+)
