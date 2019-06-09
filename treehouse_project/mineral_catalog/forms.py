from django import forms
from .models import Mineral

alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

group = [
    ('Silicates', 'Silicates'),
    ('Oxides', 'Oxides'),
    ('Sulfates', 'Sulfates'),
    ('Sulfides', 'Sulfides'),
    ('Carbonates', 'Carbonates'),
    ('Halides', 'Halides'),
    ('Sulfosalts', 'Sulfosalts'),
    ('Phosphates', 'Phosphates'),
    ('Borates', 'Borates'),
    ('Organic Minerals', 'Organic Minerals'),
    ('Arsenates', 'Arsenates'),
    ('Native Elements', 'Native Elements'),
    ('Other', 'Other'),
]


class FilterSearchForm(forms.Form):
    search = forms.CharField(max_length=255, required=False)
    letter = forms.ChoiceField(
        choices=[('------', '------')] + [(letter, letter)
                                          for letter in alphabet],
        required=False,
    )
    group = forms.ChoiceField(
        choices=[('------', '------')] + group, required=False,)
    category = forms.ChoiceField(
        choices=[('------', '------')], required=False,)
    streak = forms.ChoiceField(
        choices=[('------', '------')], required=False,)

    def __init__(self, *args, **kwargs):
        super(FilterSearchForm, self).__init__(*args, **kwargs)
        self.fields['letter'].initial = 'A'
        self.fields['group'].initial = '------'
        self.fields['category'].initial = '------'
        self.fields['streak'].initial = '------'
        # get the data needed to create labels for select element
        self.fields['category'].choices += Mineral.objects.all(
        ).order_by('category').values_list(
            'category', 'category').distinct()
        self.fields['streak'].choices += Mineral.objects.all(
        ).order_by('streak').values_list(
            'streak', 'streak').distinct()
