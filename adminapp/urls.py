from django.urls import path

import adminapp.views as adminapp


urlpatterns = [
    path('user/create/', adminapp.UserCreateView.as_view(), name='user_create'),
    path('user/read/', adminapp.UserListView.as_view(), name='user_read'),
    path('user/update/<int:pk>/', adminapp.UserUpdateView.as_view(), name='user_update'),
    path('user/delete/<int:pk>/', adminapp.UserDeleteView.as_view(), name='user_delete'),
    path('category/create/', adminapp.CategoryCreateView.as_view(), name='category_create'),
    path('category/read/', adminapp.CategoryListView.as_view(), name='category_read'),
    path('category/update/<int:pk>/', adminapp.CategoryUpdateView.as_view(), name='category_update'),
    path('category/delete/<int:pk>/', adminapp.CategoryDeleteView.as_view(), name='category_delete'),
    path('product/read/category/<int:pk>/', adminapp.ProductListView.as_view(), name='products'),
    path('product/read/<int:pk>/', adminapp.ProductDetailView.as_view(), name='product_read'),
    path('product/create/category/<int:pk>/', adminapp.product_create, name='product_create'),
    path('product/update/<int:pk>/', adminapp.product_update, name='product_update'),
    path('product/delete/<int:pk>/', adminapp.product_delete, name='product_delete'),
]