from django.urls import path
import mainapp.views as views

urlpatterns = [
    path('', views.category, name='index'),
    path('<slug:slug>/', views.category, name='category'),
    path('<slug:slug>/page/<int:page>/', views.category, name='page'),
]
