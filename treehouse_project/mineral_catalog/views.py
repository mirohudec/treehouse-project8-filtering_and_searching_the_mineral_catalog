from django.shortcuts import render

# Create your views here.


def mineral_catalog_list(request):
    return render(request, 'mineral_catalog/index.html')
