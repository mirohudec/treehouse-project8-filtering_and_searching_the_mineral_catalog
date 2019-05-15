from django.shortcuts import render

from random import choice
from .models import Mineral


def mineral_catalog_list(request):
    minerals = Mineral.objects.all().values('name')
    return render(request,
                  'mineral_catalog/index.html', {'minerals': minerals})


def mineral_detail(request, name):
    mineral = Mineral.objects.filter(name=name).values()[0]
    # filter id and empty fields out of mineral dictionary and replace
    # underscores with space (did not capitalize because project
    # instructions want to use template filter)
    mineral_fields = {}
    for key, value in mineral.items():
        if key == 'id' or value == '':
            continue
        mineral_fields[key] = (key.replace('_', ' '), value)

    return render(request, 'mineral_catalog/detail.html',
                  {'mineral': mineral_fields})
