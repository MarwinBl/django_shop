from django.urls import path

import adminapp.views as adminapp


urlpatterns = [
    path('user/create/', adminapp.user_create, name='user_create'),
    path('user/read/', adminapp.user_read, name='user_read'),
    path('user/update/<int:pk>/', adminapp.user_update, name='user_update'),
    path('user/delete/<int:pk>/', adminapp.user_delete, name='user_delete'),
    path('category/create/', adminapp.category_create, name='category_create'),
    path('category/read/', adminapp.category_read, name='category_read'),
    path('category/update/<int:pk>/', adminapp.category_update, name='category_update'),
    path('category/delete/<int:pk>/', adminapp.category_delete, name='category_delete'),
    path('product/create/category/<int:pk>/', adminapp.product_create, name='product_create'),
    path('product/read/category/<int:pk>/', adminapp.products, name='products'),
    path('product/read/<int:pk>/', adminapp.product_read, name='product_read'),
    path('product/update/<int:pk>/', adminapp.product_update, name='product_update'),
    path('product/delete/<int:pk>/', adminapp.product_delete, name='product_delete'),
]