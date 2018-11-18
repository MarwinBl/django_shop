from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage
from mainapp.models import *


def menu_decorator(func):
    def wrapper(request, *args, **kwargs):
        context_menu = {'memu_link': [
                        {'href': 'index', 'name': 'главная', 'submenu': False},
                        {'href': 'category:index', 'name': 'категории', 'submenu': Category.active_objects.all()},
                        {'href': 'contact', 'name': 'контакты', 'submenu': False},
                        ]}
        return func(request, context=context_menu, *args, **kwargs)
    return wrapper


def get_hot_product():
    return Product.objects.filter(is_active=True).order_by('-quantity').first()


def get_same_products(product):
    return Product.objects.filter(category__in=product.category.all(), is_active=True).exclude(pk=product.pk)[:3]


@menu_decorator
def index(request, context):
    context['hot_product'] = get_hot_product()
    context['same_product'] = get_same_products(context['hot_product'])
    return render(request, 'mainapp/index.html', context)


@menu_decorator
def category(request, context, slug=None, page=1):
    if slug:
        category = get_object_or_404(Category, slug=slug, is_active=True)
        products = category.product_set.filter(is_active=True).order_by('-price')
        paginator = Paginator(products, 2)
        try:
            products_paginator = paginator.page(page)
        except EmptyPage:
            products_paginator = paginator.page(paginator.num_pages)
        context['products'] = products_paginator
        context['category'] = category

        return render(request, 'mainapp/category.html', context)
    else:
        context['categories'] = Category.active_objects.all()
        return render(request, 'mainapp/categories.html', context)


@menu_decorator
def about(request, context, product):
    _product = get_object_or_404(Product, slug=product, is_active=True)
    context['product'] = _product
    return render(request, 'mainapp/about.html', context)


@menu_decorator
def contact(request, context):
    return render(request, 'mainapp/contact.html', context)