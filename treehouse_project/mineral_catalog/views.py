from django.shortcuts import render, redirect, reverse
from django.db.models import Q

from .models import Mineral
from .forms import FilterSearchForm


def mineral_catalog_list(request):
    by_letter = 'A'
    by_group = 'all'
    by_search = ''
    by_category = 'all'
    by_streak = 'all'

    data = request.GET

    form = FilterSearchForm(request.GET or None)

    # create query for searching by first letter of the mineral
    if 'letter' in data.keys():
        by_letter = data['letter']
        if by_letter != 'all':
            alphabet_Q = Q(name__startswith=by_letter)
        else:
            alphabet_Q = Q()
    else:
        alphabet_Q = Q(name__startswith=by_letter)

    # create query for searching by group
    if 'group' in data.keys():
        by_group = data['group']
        if by_group != 'all':
            group_Q = Q(group=by_group)
        else:
            group_Q = Q()
    else:
        group_Q = Q()

    # create query for searching by category
    if 'category' in data.keys():
        by_category = data['category']
        if by_category != 'all':
            category_Q = Q(category=by_category)
        else:
            category_Q = Q()
    else:
        category_Q = Q()

    # create query for searching by streak
    if 'streak' in data.keys():
        by_streak = data['streak']
        if by_streak != 'all':
            streak_Q = Q(streak=by_streak)
        else:
            streak_Q = Q()
    else:
        streak_Q = Q()

    # create query for searching by text in all of the fields in database
    if 'search' in data.keys():
        by_search = data['search']
        search_Q = (
            Q(name__icontains=by_search) |
            Q(category__icontains=by_search) |
            Q(image_filename__icontains=by_search) |
            Q(image_caption=by_search) |
            Q(formula__icontains=by_search) |
            Q(strunz_classification__icontains=by_search) |
            Q(color__icontains=by_search) |
            Q(crystal_system__icontains=by_search) |
            Q(unit_cell__icontains=by_search) |
            Q(crystal_symmetry__icontains=by_search) |
            Q(cleavage__icontains=by_search) |
            Q(mohs_scale_hardness__icontains=by_search) |
            Q(luster__icontains=by_search) |
            Q(streak__icontains=by_search) |
            Q(diaphaneity__icontains=by_search) |
            Q(optical_properties__icontains=by_search) |
            Q(refractive_index__icontains=by_search) |
            Q(crystal_habit__icontains=by_search) |
            Q(specific_gravity__icontains=by_search) |
            Q(group__icontains=by_search)
        )

    else:
        search_Q = Q()

    minerals = Mineral.objects.filter(
        alphabet_Q & group_Q & search_Q & category_Q & streak_Q)

    return render(request,
                  'mineral_catalog/index.html',
                  {'minerals': minerals,
                   'form': form
                   })


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

    form = FilterSearchForm(initial={'letter': 'all'})

    return render(request, 'mineral_catalog/detail.html',
                  {'mineral': mineral_fields,
                   'form': form
                   })
