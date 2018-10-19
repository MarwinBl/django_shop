from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import user_passes_test
from mainapp.models import Product, Category
from authapp.models import ShopUser
from authapp.forms import ShopUserRegistrationForm
from adminapp.forms import ShopUserAdminEditForm, CategoryAdminEditForm, ProductAdminEditForm


@user_passes_test(lambda u: u.is_superuser)
def user_read(request):
    users_list = ShopUser.objects.all().order_by('-is_active', '-is_superuser', '-is_staff', 'username')
    return render(request, 'adminapp/users.html', {'objects': users_list})


@user_passes_test(lambda u: u.is_superuser)
def user_create(request):
    form = ShopUserRegistrationForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and  form.is_valid():
        form.save()
        return redirect('admin:user_read')
    return render(request, 'adminapp/user_update.html', {'form': form})


@user_passes_test(lambda u: u.is_superuser)
def user_update(request, pk):
    user = get_object_or_404(ShopUser, pk=pk)
    if request.method == 'POST':
        form = ShopUserAdminEditForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('admin:user_update', pk=user.pk)
    else:
        form = ShopUserAdminEditForm(instance=user)
    return render(request, 'adminapp/user_update.html', {'form': form})


@user_passes_test(lambda u: u.is_superuser)
def user_delete(request, pk):
    user = get_object_or_404(ShopUser, pk=pk)
    if request.method == 'POST':
        user.is_active = False
        user.save()
        return redirect('admin:user_read')
    return render(request, 'adminapp/user_delete.html', {'user': user})



@user_passes_test(lambda u: u.is_superuser)
def category_read(request):
    categories_list = Category.objects.all().order_by('-is_active')
    return render(request, 'adminapp/categories.html', {'objects': categories_list})


@user_passes_test(lambda u: u.is_superuser)
def category_create(request):
    form = CategoryAdminEditForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
    return render(request, 'adminapp/category_update.html', {'form': form})


@user_passes_test(lambda u: u.is_superuser)
def category_update(request, pk):
    model = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        form = CategoryAdminEditForm(request.POST, instance=model)
        if form.is_valid():
            form.save()
            return redirect('admin:category_read')
        else:
            return render(request, 'adminapp/category_update.html', {'form': form})
    form = CategoryAdminEditForm(instance=model)
    return render(request, 'adminapp/category_update.html', {'form': form})


@user_passes_test(lambda u: u.is_superuser)
def category_delete(request, pk):
    model = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        model.is_active=False
        model.save()
        return redirect('admin:category_read')
    return render(request, 'adminapp/category_delete.html', {'model': model})


@user_passes_test(lambda u: u.is_superuser)
def products(request, pk):

    category = get_object_or_404(Category, pk=pk)
    products_list = Product.objects.filter(category__pk=pk).order_by('name')

    content = {
        'category': category,
        'objects': products_list,
    }

    return render(request, 'adminapp/products.html', content)


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
def product_read(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'adminapp/product_read.html', {'product': product})


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

