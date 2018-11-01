from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.contrib.auth.decorators import user_passes_test
from mainapp.models import Product, Category
from authapp.models import ShopUser
from authapp.forms import ShopUserRegistrationForm
from adminapp.forms import ShopUserAdminEditForm, CategoryAdminEditForm, ProductAdminEditForm
from .utils import AdminListView, AdminCreateView, AdminUpdateView, AdminDetailView, AdminDeleteView


class UserListView(AdminListView):
    model = ShopUser
    template_name = 'adminapp/users.html'
    ordering = ('-is_active', '-is_superuser', '-is_staff', 'username')


class UserCreateView(AdminCreateView):
    form_class = ShopUserRegistrationForm
    template_name = 'adminapp/user_update.html'
    success_url = reverse_lazy('admin:user_read')


class UserUpdateView(AdminUpdateView):
    form_class = ShopUserAdminEditForm
    model = ShopUser
    template_name = 'adminapp/user_update.html'
    success_url = reverse_lazy('admin:user_read')


class UserDeleteView(AdminDeleteView):
    model = ShopUser
    template_name = 'adminapp/user_delete.html'
    success_url = reverse_lazy('admin:user_read')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = False
        self.object.save()
        return redirect(self.success_url)


class CategoryListView(AdminListView):
    model = Category
    template_name = 'adminapp/categories.html'
    ordering = ('-is_active', 'name')


class CategoryCreateView(AdminCreateView):
    form_class = CategoryAdminEditForm
    template_name = 'adminapp/category_update.html'
    success_url = reverse_lazy('admin:category_read')


class CategoryUpdateView(AdminUpdateView):
    form_class = CategoryAdminEditForm
    model = Category
    template_name = 'adminapp/category_update.html'
    success_url = reverse_lazy('admin:category_read')


class CategoryDeleteView(AdminDeleteView):
    model = Category
    template_name = 'adminapp/category_delete.html'
    success_url = reverse_lazy('admin:category_read')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = False
        self.object.save()
        return redirect(self.success_url)


class ProductListView(AdminListView):
    template_name = 'adminapp/products.html'
    paginate_by = 4

    def get_queryset(self):
        pk = self.kwargs.get('pk', None)
        return Product.objects.filter(category__pk=pk).order_by('name')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs.get('pk', None)
        context['category'] = get_object_or_404(Category, pk=pk)
        return context


class ProductDetailView(AdminDetailView):
    model = Product
    template_name = 'adminapp/product_read.html'


class ProductCreateView(AdminCreateView):
    form_class = ProductAdminEditForm
    template_name = 'adminapp/product_update.html'

    def get_success_url(self):
        return reverse_lazy('admin:products', kwargs={'pk': self.kwargs.get('pk')})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs.get('pk', None)
        context['category'] = get_object_or_404(Category, pk=pk)
        return context


class ProductUpdateView(AdminUpdateView):
    form_class = ProductAdminEditForm
    model = Product
    template_name = 'adminapp/product_update.html'

    def get_success_url(self):
        return reverse_lazy('admin:product_read', kwargs={'pk': self.kwargs.get('pk')})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = self.object.category.all()
        return context


class ProductDeleteView(AdminDeleteView):
    model = Product
    template_name = 'adminapp/product_delete.html'

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = False
        self.object.save()
        return redirect('admin:products', pk=self.object.category.first().pk)
