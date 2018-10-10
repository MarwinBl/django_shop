from django.shortcuts import render
from mainapp.models import *


MENU = (
    {'href': 'index', 'name': 'главная', 'submenu': False},
    {'href': 'category:index', 'name': 'категории', 'submenu': Category.objects.all()},
    {'href': 'contact', 'name': 'контакты', 'submenu': False},
)

context = {'memu_link': MENU}


def index(request):
    products = Product.objects.all()[:3]
    context['products'] = products
    return render(request, 'mainapp/index.html', context)


def categories(request):
    _categories = Category.objects.all()
    context['categories'] = _categories
    return render(request, 'mainapp/categories.html', context)


def category(request, slug):
    _category = Category.objects.get(slug=slug)
    context['category'] = _category
    return render(request, 'mainapp/category.html', context)


def about(request, product):
    _product = Product.objects.get(name=product)
    context['product'] = _product
    return render(request, 'mainapp/about.html', context)


def contact(request):
    return render(request, 'mainapp/contact.html', context)