from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
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
    success_url = reverse_lazy('admin:user_read')


class UserUpdateView(AdminUpdateView):
    form_class = ShopUserAdminEditForm
    model = ShopUser
    success_url = reverse_lazy('admin:user_read')


class UserDeleteView(AdminDeleteView):
    model = ShopUser
    template_name = 'adminapp/object_del_or_restore.html'
    success_url = 'admin:user_read'


class UserRestoreView(AdminDeleteView):
    model = ShopUser
    template_name = 'adminapp/object_del_or_restore.html'
    success_url = 'admin:user_read'
    is_active = True


class CategoryListView(AdminListView):
    model = Category
    template_name = 'adminapp/categories.html'
    ordering = ('-is_active', 'name')


class CategoryCreateView(AdminCreateView):
    form_class = CategoryAdminEditForm
    success_url = reverse_lazy('admin:category_read')


class CategoryUpdateView(AdminUpdateView):
    form_class = CategoryAdminEditForm
    model = Category
    success_url = reverse_lazy('admin:category_read')


class CategoryDeleteView(AdminDeleteView):
    model = Category
    template_name = 'adminapp/object_del_or_restore.html'
    success_url = 'admin:category_read'


class CategoryRestoreView(AdminDeleteView):
    model = Category
    template_name = 'adminapp/object_del_or_restore.html'
    success_url = 'admin:category_read'
    is_active = True


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

    def get_success_url(self):
        return reverse_lazy('admin:products', kwargs={'pk': self.kwargs.get('pk')})


class ProductUpdateView(AdminUpdateView):
    form_class = ProductAdminEditForm
    model = Product

    def get_success_url(self):
        return reverse_lazy('admin:product_read', kwargs={'pk': self.kwargs.get('pk')})


class ProductDeleteView(AdminDeleteView):
    model = Product
    template_name = 'adminapp/object_del_or_restore.html'
    success_url = 'admin:products'

    def get_success_url_kwargs(self):
        return {'pk': self.object.category.first().pk}


class ProductRestoreView(AdminDeleteView):
    model = Product
    template_name = 'adminapp/object_del_or_restore.html'
    success_url = 'admin:products'
    is_active = True

    def get_success_url_kwargs(self):
        return {'pk': self.object.category.first().pk}

