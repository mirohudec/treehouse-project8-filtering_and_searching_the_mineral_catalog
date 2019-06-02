from django.test import TestCase
from django.urls import reverse

from mineral_catalog.models import Mineral
from mineral_catalog.forms import FilterSearchForm

# coverage run --source='.' manage.py test


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
            name="Abelsonite",
            image_filename="Abelsonite.jpg",
            image_caption="Abelsonite from the Green River Formation, Uintah County, Utah, US",
            category="Organic",
            formula="C<sub>31</sub>H<sub>32</sub>N<sub>4</sub>Ni",
            strunz_classification="10.CA.20",
            crystal_system="Triclinic",
            unit_cell="a = 8.508 \u00c5, b = 11.185 \u00c5c=7.299 \u00c5, \u03b1 = 90.85\u00b0\u03b2 = 114.1\u00b0, \u03b3 = 79.99\u00b0Z = 1",
            color="Pink-purple, dark greyish purple, pale purplish red, reddish brown",
            crystal_symmetry="Space group: P1 or P1Point group: 1 or 1",
            cleavage="Probable on {111}",
            mohs_scale_hardness="2\u20133",
            luster="Adamantine, sub-metallic",
            streak="Pink",
            diaphaneity="Semitransparent",
            optical_properties="Biaxial",
            group="Organic Minerals"
        )
        self.mineral2 = Mineral.objects.create(
            name="Metacinnabar",
            image_filename="Metacinnabar.jpg",
            image_caption="Metacinnabar collected from Mount Diablo Mine, Mount Diablo, Clayton, California",
            category="Sulfide",
            formula="HgS",
            strunz_classification="2.CB.05a",
            crystal_system="Cubic",
            unit_cell="a = 5.8717(5) \u00c5; Z=4",
            color="Grayish black",
            crystal_symmetry="Isometric hextetrahedralH-M symbol: (43m)Space group: F43m",
            cleavage="None",
            mohs_scale_hardness="3",
            luster="Metallic",
            streak="Black",
            diaphaneity="Opaque",
            crystal_habit="Massive, rarely as tetrahedral crystals, as incrustations",
            specific_gravity="7.7 - 7.8",
            group="Sulfides"
        )
        self.mineral3 = Mineral.objects.create(
            name="Ulexite",
            image_filename="Ulexite.jpg",
            image_caption="Ulexite from California (size: 6.9 \u00d7 5 \u00d7 3.1 cm)",
            category="Nesoborates",
            formula="NaCaB<sub>5</sub>O<sub>6</sub>(OH)<sub>6</sub>\u00b7<sub>5</sub>H<sub>2</sub>O",
            strunz_classification="06.EA.25",
            crystal_system="Triclinic - pinacoidal",
            unit_cell="a = 8.816(3) \u00c5, b = 12.87\u00c5, c = 6.678(1) \u00c5; \u03b1 = 90.25\u00b0, \u03b2 = 109.12\u00b0, \u03b3 = 105.1\u00b0; Z = 2",
            color="Colorless to white",
            crystal_symmetry="Triclinic P1 (1)",
            cleavage="Perfect on {010} good on {110} poor on {110}",
            mohs_scale_hardness="2.5",
            luster="Vitreous; silky or satiny in fibrous aggregates",
            streak="White",
            diaphaneity="Transparent to opaque",
            optical_properties="Biaxial (+)",
            refractive_index="n\u03b1 = 1.491 \u2013 1.496n\u03b2 = 1.504 \u2013 1.506 br/>n\u03b3 = 1.519 \u2013 1.520",
            crystal_habit="Acicular to fibrous",
            specific_gravity="1.95 \u2013 1.96",
            group="Borates"
        )

    def test_mineral_catalog_list_view(self):
        response = self.client.get(reverse('mineral_catalog:list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'mineral_catalog/index.html')
        # first response is with filter for letter A
        self.assertEqual(len(response.context['minerals']), 1)

    def test_mineral_catalog_list_by_group(self):
        response = self.client.get(reverse('mineral_catalog:list'), data={
            'letter': 'all',
            'group': 'Borates',
            'category': 'all',
            'streak': 'all',
            'search': ''
        })
        query_string = response.request['QUERY_STRING']
        self.assertTrue('group=Borates' in query_string)
        self.assertEqual(len(response.context['minerals']), 1)
        self.assertEqual(response.context['minerals'][0].name, 'Ulexite')

    def test_mineral_catalog_list_by_category(self):
        response = self.client.get(reverse('mineral_catalog:list'), data={
            'letter': 'all',
            'group': 'all',
            'category': 'Sulfide',
            'streak': 'all',
            'search': ''
        })
        query_string = response.request['QUERY_STRING']
        self.assertTrue('category=Sulfide' in query_string)
        self.assertEqual(len(response.context['minerals']), 1)
        self.assertEqual(response.context['minerals'][0].name, 'Metacinnabar')

    def test_mineral_catalog_list_by_streak(self):
        response = self.client.get(reverse('mineral_catalog:list'), data={
            'letter': 'all',
            'group': 'all',
            'category': 'all',
            'streak': 'White',
            'search': ''
        })
        query_string = response.request['QUERY_STRING']
        self.assertTrue('streak=White' in query_string)
        self.assertEqual(len(response.context['minerals']), 1)
        self.assertEqual(response.context['minerals'][0].name, 'Ulexite')

    def test_mineral_catalog_list_by_search(self):
        response = self.client.get(reverse('mineral_catalog:list'), data={
            'letter': 'all',
            'group': 'all',
            'category': 'all',
            'streak': 'all',
            'search': 'Triclinic'
        })
        query_string = response.request['QUERY_STRING']
        self.assertTrue('search=Triclinic' in query_string)
        self.assertEqual(len(response.context['minerals']), 2)
        self.assertEqual(response.context['minerals'][0].name, 'Abelsonite')
        self.assertEqual(response.context['minerals'][1].name, 'Ulexite')

    def test_mineral_catalog_list_by_search_and_category(self):
        response = self.client.get(reverse('mineral_catalog:list'), data={
            'letter': 'all',
            'group': 'all',
            'category': 'Nesoborates',
            'streak': 'all',
            'search': 'Triclinic'
        })
        query_string = response.request['QUERY_STRING']
        self.assertTrue('search=Triclinic' in query_string)
        self.assertTrue('category=Nesoborates' in query_string)
        self.assertEqual(len(response.context['minerals']), 1)
        self.assertEqual(response.context['minerals'][0].name, 'Ulexite')

    def test_mineral_detail_view(self):
        response = self.client.get(
            reverse('mineral_catalog:detail',
                    kwargs={'name': 'Ulexite'}))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'mineral_catalog/detail.html')
        self.assertEqual('Ulexite', response.context['mineral']['name'][1])
