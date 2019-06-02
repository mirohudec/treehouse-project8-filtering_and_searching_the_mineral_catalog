import os
import json

from django.core.management.base import BaseCommand
from mineral_catalog.models import Mineral


class Command(BaseCommand):
    # https://stackoverflow.com/questions/53579677/django-2-1-how-to-import-models-in-a-custom-py-file

    help = 'populate database with minerals from mineral.json in static/data'

    def handle(self, *args, **options):
        path = os.path.join(os.path.dirname(os.getcwd()),
                            'treehouse_project/mineral_catalog/' +
                            'static/mineral_catalog/data/minerals.json')
        with open(path) as json_data:
            data = json.load(json_data)

        for mineral_data in data:
            try:
                Mineral.objects.create(**mineral_data)
            except:
                breakpoint()
