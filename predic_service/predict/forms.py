from django import forms
from django.forms.widgets import NumberInput, RadioSelect

class PredictForm(forms.Form):
    rooms = forms.FloatField(min_value=0, max_value=5)
    square = forms.FloatField(min_value=1)
    kitchen_scace = forms.FloatField(min_value=1)
    serv_lift = forms.BooleanField(required=False)
    curr_floor = forms.FloatField(min_value=0)
    max_value = forms.FloatField(min_value=0)
    pass_lift = forms.BooleanField(required=False)
    parking = forms.BooleanField(required=False)
    loggia = forms.BooleanField(required=False)
    balcony = forms.BooleanField(required=False)
    garbage_chute = forms.BooleanField(required=False)
    bathroom = forms.BooleanField(required=False)
    district = forms.ChoiceField(choices=(('Железнодорожный', 'Железнодорожный р-н'),
                                          ('Кировский', 'Кировский р-н'),
                                          ('Ленинский', 'Ленинский р-н'),
                                          ('Октябрьский', 'Октябрьский р-н'),
                                          ('Первомайский', 'Первомайский р-н'),
                                          ('Пролетарский', 'Пролетарский р-н'),
                                          ('Советский', 'Советский р-н')))
    home_type = forms.ChoiceField(choices=(('Блочный', 'Блочный'),
                                           ('Кирпичный', 'Кирпичный'),
                                           ('Монолитный', 'Монолитный'),
                                           ('Панельный', 'Панельный')))
    repair_type = forms.ChoiceField(choices=(('Без ремонта', 'Без ремонта'),
                                             ('Дизайнерский', 'Дизайнерский'),
                                             ('Евроремонт', 'Евроремонт'),
                                             ('Косметический', 'Косметический')))
    # count = forms.IntegerField(min_value=0, max_value=100, widget=NumberInput(attrs={'type':'range', 'step': '1'}))
