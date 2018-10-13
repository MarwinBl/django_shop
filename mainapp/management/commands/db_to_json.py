from decimal import Decimal
from django.conf import settings
from django.core.management.base import BaseCommand
from django.forms.models import model_to_dict
from django.db.models.fields.files import ImageFieldFile
from mainapp.models import *

import json, os


JSON_PATH = os.path.join(settings.BASE_DIR, 'mainapp', 'json')


def load_to_json(file_name, field_list):
    with open(os.path.join(JSON_PATH, file_name + '.json'), 'w', encoding='UTF-8') as file:
        file.write(json.dumps(field_list, ensure_ascii=False))


def end_filter(field_list):

    for row in field_list:
        for field, val in row.items():
            if isinstance(val, ImageFieldFile):
                row[field] = val.url
            if isinstance(val, Decimal):
                row[field] = float(val)
            if isinstance(val, list):
                for i, item in enumerate(val):
                    if isinstance(item, Category):
                        val[i] = item.name
    return field_list


class Command(BaseCommand):

    def handle(self, *args, **options):
        categories = [model_to_dict(category) for category in Category.objects.all()]
        load_to_json('categories', categories)

        products = [model_to_dict(product) for product in Product.objects.all()]
        load_to_json('products', end_filter(products))