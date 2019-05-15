from django.test import TestCase
from django.urls import reverse

from mineral_catalog.models import Mineral


class MineralModelTests(TestCase):
    def test_mineral_created_successfuly(self):
        data = {
            'name': 'Abelsonite',
            'category': 'Organic',
            'group': 'Organic Materials',
            'crystal_system': 'Triclinic',
            'mohs_scale_hardness': '2-3',
            'streak': 'Pink',
            'diaphaneity': 'Semitransparent',
        }
        mineral = Mineral.objects.create(**data)
        self.assertEqual(data['name'], mineral.name)
        self.assertEqual(data['group'], mineral.group)
        self.assertEqual(data['diaphaneity'], mineral.diaphaneity)

    def test_mineral_creation_failed(self):
        data = {
            'fullname': 'Abelsonite',
            'category': 'Organic',
            'group': 'Organic Materials',
            'crystal_system': 'Triclinic',
            'mohs_scale_hardness': '2-3',
            'streak': 'Pink',
            'diaphaneity': 'Semitransparent',
        }
        with self.assertRaises(TypeError):
            Mineral.objects.create(**data)


class MineralCatalogViewsTests(TestCase):
    def setUp(self):
        self.mineral = Mineral.objects.create(
            name='Chromite'
        )
        self.mineral2 = Mineral.objects.create(
            name='Hessite'
        )
        self.mineral3 = Mineral.objects.create(
            name='Adamite'
        )

    def test_mineral_catalog_list_view(self):
        response = self.client.get(reverse('mineral_catalog:list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'mineral_catalog/index.html')
        self.assertEqual(len(response.context['minerals']), 3)

    def test_mineral_detail_view(self):
        response = self.client.get(
            reverse('mineral_catalog:detail',
                    kwargs={'name': 'Chromite'}))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'mineral_catalog/detail.html')
        self.assertEqual('Chromite', response.context['mineral']['name'][1])
