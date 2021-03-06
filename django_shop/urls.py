"""django_shop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

import mainapp.views as mainapp

urlpatterns = [
    path('admin/', include(('adminapp.urls', 'adminapp'), namespace='admin')),
    path('auth/', include(('authapp.urls', 'authapp'), namespace='auth')),

    path('', mainapp.index, name='index'),
    path('contact/', mainapp.contact, name='contact'),
    path('about/<str:product>/', mainapp.about, name='about'),
    path('category/', include(('mainapp.urls', 'mainapp'), namespace='category')),
    path('basket/', include(('basketapp.urls', 'basketapp'), namespace='basket')),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
