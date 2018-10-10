from django.urls import re_path, path
import mainapp.views as views

urlpatterns = [
    path('', views.categories, name='index'),
    path('<slug:slug>/', views.category, name='category'),
]
