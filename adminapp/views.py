from django.db import transaction
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from mainapp.models import Product, Category
from authapp.models import ShopUser
from authapp.forms import ShopUserRegistrationForm
from adminapp.forms import ShopUserAdminEditForm, CategoryAdminEditForm, ProductAdminEditForm
from orderapp.forms import OrderForm
from orderapp.models import Order
from orderapp.views import FormSetMixin
from .utils import AdminListView, AdminCreateView, AdminUpdateView, AdminDetailView, AdminDeleteView, AdminAjaxConfirmView


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
    success_url = 'admin:user_read'


class UserRestoreView(AdminDeleteView):
    model = ShopUser
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
    success_url = 'admin:category_read'


class CategoryRestoreView(AdminDeleteView):
    model = Category
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
    success_url = 'admin:products'

    def get_success_url_kwargs(self):
        return {'pk': self.object.category.first().pk}


class ProductRestoreView(AdminDeleteView):
    model = Product
    success_url = 'admin:products'
    is_active = True

    def get_success_url_kwargs(self):
        return {'pk': self.object.category.first().pk}


class AjaxGeneralConfirm(AdminAjaxConfirmView):
    models_dict = {
        'user': ShopUser,
        'category': Category,
        'product': Product
    }


class OrderListView(AdminListView):
    template_name = 'adminapp/order_list.html'
    model = Order


class OrderUpdateView(FormSetMixin, AdminUpdateView):
    template_name = 'adminapp/order_update.html'
    model = Order
    form_class = OrderForm
    success_url = reverse_lazy('admin:order_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['orderitems'] = (self.get_formset_from_post(instance=True)
                                 if self.request.POST
                                 else self.get_formset(formsetkwargs={'instance': self.object}))
        return context

    def form_valid(self, form):
        formset = self.get_formset_from_post(instance=True)
        with transaction.atomic():
            self.object = form.save()
            if formset.is_valid():
                formset.instance = self.object
                formset.save()

        if self.object.get_total_cost() == 0:
            self.object.delete()
        return super().form_valid(form)


class OrderDeleteView(AdminDeleteView):
    model = Order
    success_url = 'admin:order_list'