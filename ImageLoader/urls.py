"""ImageLoader URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from ImageLoader import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('load/', views.CreateImageView.as_view(), name='new_image'),
    path('', views.ImageListView.as_view(), name='image_list'),
    path('resize/<pk>/', views.ImageResizeView.as_view(), name='resize_image'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
