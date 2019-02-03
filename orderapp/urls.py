from django.urls import path
import orderapp.views as views

urlpatterns = [
    path('', views.OrderList.as_view(), name='list'),
    path('forming/complete/<int:pk>/', views.forming_complete, name='forming_complete'),
    path('create/', views.OrderCreate.as_view(), name='create'),
    path('read/<int:pk>/', views.OrderRead.as_view(), name='read'),
    path('update/<int:pk>/', views.OrderUpdate.as_view(), name='update'),
    path('delete/<int:pk>/', views.OrderDelete.as_view(), name='delete'),
]
