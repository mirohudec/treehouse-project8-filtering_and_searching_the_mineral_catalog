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

category_qs = Mineral.objects.all().order_by(
    'category').distinct().values('category')
category = [(category['category'], category['category'])
            for category in category_qs]

streak_qs = Mineral.objects.all().order_by(
    'streak').distinct().values('streak')
streak = [(streak['streak'], streak['streak']) for streak in streak_qs]


class FilterSearchForm(forms.Form):
    search = forms.CharField(max_length=255, required=False)
    letter = forms.ChoiceField(
        choices=[('all', 'all')] + [(letter, letter) for letter in alphabet],
        widget=forms.Select(attrs={"onChange": 'this.form.submit()'}),
        required=False,
        )
    group = forms.ChoiceField(choices=[('all', 'all')] + group, widget=forms.Select(
        attrs={"onChange": 'this.form.submit()'}), required=False)
    category = forms.ChoiceField(
        choices=[('all', 'all')] + category, widget=forms.Select(attrs={"onChange": 'this.form.submit()'}), required=False)
    streak = forms.ChoiceField(
        choices=[('all', 'all')] + streak, widget=forms.Select(attrs={"onChange": 'this.form.submit()'}), required=False)

    def __init__(self, *args, **kwargs):
        super(FilterSearchForm, self).__init__(*args, **kwargs)
        self.fields['letter'].initial = 'A'
        self.fields['group'].initial = 'all'
        self.fields['category'].initial = 'all'
        self.fields['streak'].initial = 'all'
