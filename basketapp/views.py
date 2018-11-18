from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from mainapp.models import Product
from basketapp.models import Basket


def get_basket(user):
    if user.is_authenticated:
        return Basket.get_total_count_and_price(user=user)


def ajax_response(request, name, quantity):
    return JsonResponse({
        'name': name,
        'quantity': quantity,
        'basket': get_basket(request.user)
    })


@login_required
def index(request):
    basket_items = Basket.objects.filter(user=request.user)
    context = {
        'basket_items': basket_items,
        'basket': get_basket(request.user),
    }
    return render(request, 'basketapp/basket.html', context=context)


@login_required
def add_product(request, slug):
    product = get_object_or_404(Product, slug=slug)
    exists_item = Basket.objects.filter(user=request.user, product=product).first()
    if exists_item:
        exists_item.quantity += 1
        exists_item.save()
    else:
        exists_item = Basket(product=product, user=request.user)
        exists_item.save()
    item = exists_item

    if request.is_ajax():
        return ajax_response(request, item.product.slug, item.quantity)

    if 'login' in request.META.get('HTTP_REFERER'):
        return redirect('about', product=slug)
    return redirect(request.META.get('HTTP_REFERER'))


@login_required
def del_product(request, slug, quantity):
    is_delete = False
    basket_item = get_object_or_404(Basket, user=request.user, product__slug=slug)
    if basket_item.quantity - quantity <= 0:
        basket_item.delete()
        is_delete = True
    else:
        basket_item.quantity = basket_item.quantity - quantity
        basket_item.save()

    if request.is_ajax():
        return ajax_response(request, basket_item.product.slug, 0 if is_delete else basket_item.quantity)

    return redirect(request.META.get('HTTP_REFERER'))
