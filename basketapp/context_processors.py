from .models import Basket


def basket(request):
    if request.user.is_authenticated:
        return {'basket': Basket.get_total_count_and_price(user=request.user)}
    return {'basket': []}