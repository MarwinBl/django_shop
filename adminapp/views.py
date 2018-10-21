from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.contrib.auth.decorators import user_passes_test
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from mainapp.models import Product, Category
from authapp.models import ShopUser
from authapp.forms import ShopUserRegistrationForm
from adminapp.forms import ShopUserAdminEditForm, CategoryAdminEditForm, ProductAdminEditForm
from .utils import AdminListView


class UserListView(AdminListView):
    model = ShopUser
    template_name = 'adminapp/users.html'
    ordering = ('-is_active', '-is_superuser', '-is_staff', 'username')


class UserCreateView(CreateView):
    form_class = ShopUserRegistrationForm
    template_name = 'adminapp/user_update.html'
    success_url = reverse_lazy('admin:user_read')


class UserUpdateView(UpdateView):
    form_class = ShopUserAdminEditForm
    model = ShopUser
    template_name = 'adminapp/user_update.html'
    success_url = reverse_lazy('admin:user_read')


class UserDeleteView(DeleteView):
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
    ordering = '-is_active'


class CategoryCreateView(CreateView):
    form_class = CategoryAdminEditForm
    template_name = 'adminapp/category_update.html'
    success_url = reverse_lazy('admin:category_read')


class CategoryUpdateView(UpdateView):
    form_class = CategoryAdminEditForm
    model = Category
    template_name = 'adminapp/category_update.html'
    success_url = reverse_lazy('admin:category_read')


class CategoryDeleteView(DeleteView):
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


class ProductDetailView(DetailView):
    model = Product
    template_name = 'adminapp/product_read.html'


@user_passes_test(lambda u: u.is_superuser)
def product_create(request, pk):
    category = get_object_or_404(Category, pk=pk)

    if request.method == 'POST':
        product_form = ProductAdminEditForm(request.POST, request.FILES)
        if product_form.is_valid():
            product_form.save()
            return redirect('admin:products', pk=pk)
    else:
        product_form = ProductAdminEditForm(initial={'category': category})

    content = {
        'form': product_form,
        'category': category
        }

    return render(request, 'adminapp/product_update.html', content)


@user_passes_test(lambda u: u.is_superuser)
def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        product_form = ProductAdminEditForm(request.POST, request.FILES, instance=product)
        if product_form.is_valid():
            product_form.save()
            return redirect('admin:product_read', pk=pk)
    else:
        product_form = ProductAdminEditForm(instance=product)

    content = {
               'form': product_form,
               'categories': product.category.all(),
               }

    return render(request, 'adminapp/product_update.html', content)


@user_passes_test(lambda u: u.is_superuser)
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        product.is_active = False
        product.save()
        return redirect('admin:products', pk=product.category.first().pk)

    return render(request, 'adminapp/product_delete.html', {'product': product})

