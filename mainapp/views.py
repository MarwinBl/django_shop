from django.shortcuts import render, get_object_or_404
from mainapp.models import *
from basketapp.views import get_basket, get_hot_product, get_same_products


MENU = (
    {'href': 'index', 'name': 'главная', 'submenu': False},
    {'href': 'category:index', 'name': 'категории', 'submenu': Category.objects.filter(is_active=True)},
    {'href': 'contact', 'name': 'контакты', 'submenu': False},
)

context = {'memu_link': MENU}


def index(request):
    context['basket'] = get_basket(request.user)
    context['hot_product'] = get_hot_product()
    context['same_product'] = get_same_products(context['hot_product'])
    return render(request, 'mainapp/index.html', context)


def category(request, slug=None):
    context['basket'] = get_basket(request.user)
    if slug:
        _category = get_object_or_404(Category, slug=slug, is_active=True)
        context['category'] = _category
        return render(request, 'mainapp/category.html', context)
    else:
        _categories = Category.objects.filter(is_active=True)
        context['categories'] = _categories
        return render(request, 'mainapp/categories.html', context)


def about(request, product):
    context['basket'] = get_basket(request.user)
    _product = get_object_or_404(Product, name=product)
    context['product'] = _product
    return render(request, 'mainapp/about.html', context)


def contact(request):
    context['basket'] = get_basket(request.user)
    return render(request, 'mainapp/contact.html', context)