from django.urls import path

from . import views

app_name = 'mineral_catalog'

urlpatterns = [
    path('', views.mineral_catalog_list, name='mineral_list')
]
