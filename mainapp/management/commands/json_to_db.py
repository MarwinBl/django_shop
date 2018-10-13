from django.conf import settings
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from mainapp.models import *

import json, os


JSON_PATH = os.path.join(settings.BASE_DIR, 'mainapp', 'json')


def load_from_json(file_name):
    with open(os.path.join(JSON_PATH, file_name + '.json'), 'r') as file:
        return json.load(file)


class Command(BaseCommand):

    def handle(self, *args, **options):
        categories = load_from_json('categories')

        Category.objects.all().delete()
        for category in categories:
            Category(**category).save()

        products = load_from_json('products')

        Product.objects.all().delete()
        for product in products:
            categories_model = []
            for cat in product['category']:
                category_model = Category.objects.get(name=cat)
                if category_model:
                    categories_model.append(category_model)
            if product['image'].startswith(settings.MEDIA_URL):
                product['image'] = product['image'][6:]
            product.pop('category')
            product = Product.objects.create(**product)
            product.category.set(categories_model)
            product.save()

        User.objects.create_superuser('django2', 'django@geekshop.local', 'geekbrains')