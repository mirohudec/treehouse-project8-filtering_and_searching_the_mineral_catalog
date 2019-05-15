from mineral_catalog.models import Mineral
from django import template
from random import choice

register = template.Library()


data = Mineral.objects.all().values('name')


@register.filter('random')
def random(args):
    """get random mineral name from all minerals in database"""
    mineral_list = list(data)
    mineral = choice(mineral_list)['name']
    return mineral
