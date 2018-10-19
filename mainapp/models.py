from django.db import models
from django.shortcuts import reverse


class Category(models.Model):
    name = models.CharField(verbose_name='Название', max_length=64, unique=True)
    slug = models.SlugField(max_length=150, unique=True)
    description = models.TextField(verbose_name='Описание', blank=True)
    is_active = models.BooleanField(verbose_name='активна', default=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ManyToManyField(Category)
    name = models.CharField(verbose_name='Название продукта', max_length=128, unique=True)
    slug = models.SlugField(max_length=150, unique=True)
    image = models.ImageField(upload_to='product_imeges', default='product_imeges/default_product.png')
    short_desc = models.CharField(verbose_name='Короткое описание', max_length=60, blank=True)
    description = models.TextField(verbose_name='Описание', blank=True)
    price = models.DecimalField(verbose_name='Цена', max_digits=8, decimal_places = 2, default = 0)
    quantity = models.PositiveIntegerField(verbose_name='Колличество', default=0)
    add_date = models.DateTimeField(auto_now_add=True)
    change_date = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def get_absolute_url(self):
        return reverse('about', kwargs={'product': self.slug})

    def __str__(self):
        return self.name