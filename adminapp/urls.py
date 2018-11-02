from django.urls import path

import adminapp.views as adminapp


urlpatterns = [
    path('user/create/', adminapp.UserCreateView.as_view(), name='user_create'),
    path('user/read/', adminapp.UserListView.as_view(), name='user_read'),
    path('user/update/<int:pk>/', adminapp.UserUpdateView.as_view(), name='user_update'),
    path('user/delete/<int:pk>/', adminapp.UserDeleteView.as_view(), name='user_delete'),
    path('user/restore/<int:pk>/', adminapp.UserRestoreView.as_view(), name='user_restore'),
    path('category/create/', adminapp.CategoryCreateView.as_view(), name='category_create'),
    path('category/read/', adminapp.CategoryListView.as_view(), name='category_read'),
    path('category/update/<int:pk>/', adminapp.CategoryUpdateView.as_view(), name='category_update'),
    path('category/delete/<int:pk>/', adminapp.CategoryDeleteView.as_view(), name='category_delete'),
    path('category/restore/<int:pk>/', adminapp.CategoryRestoreView.as_view(), name='category_restore'),
    path('product/read/category/<int:pk>/', adminapp.ProductListView.as_view(), name='products'),
    path('product/read/<int:pk>/', adminapp.ProductDetailView.as_view(), name='product_read'),
    path('product/create/category/<int:pk>/', adminapp.ProductCreateView.as_view(), name='product_create'),
    path('product/update/<int:pk>/', adminapp.ProductUpdateView.as_view(), name='product_update'),
    path('product/delete/<int:pk>/', adminapp.ProductDeleteView.as_view(), name='product_delete'),
    path('product/restore/<int:pk>/', adminapp.ProductRestoreView.as_view(), name='product_restore'),
    path('ajax/confirm/', adminapp.AjaxGeneralConfirm.as_view(), name='ajax_confirm'),
]