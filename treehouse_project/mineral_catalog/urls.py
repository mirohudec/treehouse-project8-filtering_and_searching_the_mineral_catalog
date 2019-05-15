from django.urls import path

from . import views

app_name = 'mineral_catalog'

urlpatterns = [
    path('', views.mineral_catalog_list, name='list'),
    path('<str:name>/', views.mineral_detail, name='detail'),
]
