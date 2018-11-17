from datetime import timedelta
from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import AbstractUser


class ShopUser(AbstractUser):
    avatar = models.ImageField(upload_to='users_avatar', default='users_avatar/default_user.png')
    age = models.PositiveSmallIntegerField(verbose_name='Возраст')
    activation_key = models.CharField(max_length=128, blank=True)
    activation_key_expires = models.DateTimeField(default=(now() + timedelta(hours=48)))

    def activation_key_expired(self):
        if now() <= self.activation_key_expires:
            return False
        else:
            return True
