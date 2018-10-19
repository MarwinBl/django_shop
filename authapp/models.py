from django.db import models
from django.contrib.auth.models import AbstractUser


class ShopUser(AbstractUser):
    avatar = models.ImageField(upload_to='users_avatar', default='users_avatar/default_user.png')
    age = models.PositiveSmallIntegerField(verbose_name='Возраст')