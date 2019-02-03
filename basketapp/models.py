from django.db import models
from django.contrib.auth import get_user_model
from mainapp.models import Product


class Basket(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='basket')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(verbose_name='количество', default=1)
    add_datetime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return 'Корзина {}'.format(self.user.username)

    @staticmethod
    def get_total_count_and_price(user):
        items = Basket.objects.filter(user=user)
        if items:
            res = {'count': 0, 'total_price': 0}
            for item in items:
                res['count'] += item.quantity
                res['total_price'] += item.quantity * item.product.price
            return res
    @classmethod
    def get_items(cls, user):
        return cls.objects.filter(user=user)
