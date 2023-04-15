import json

import requests
from django import forms
from django.utils.translation import gettext_lazy as _
from orders.models import Order

url = 'https://parseapi.back4app.com/classes/City?limit=5&order=-population,name&keys=name,country,countryCode,cityId,objectId'


class OrderForm(forms.ModelForm):
    first_name = forms.CharField(label='First Name', widget=forms.TextInput(
        attrs={'class': 'input-text', 'placeholder': _('First Name'), 'autocomplete': 'given-name'}))
    last_name = forms.CharField(label='Last Name', widget=forms.TextInput(
        attrs={'class': 'input-text', 'placeholder': _('Last Name'), 'autocomplete': 'family-name'}))
    address = forms.CharField(label='House number and street name', widget=forms.TextInput(
        attrs={'class': 'input-text', 'placeholder': _('House number and street name'), 'autocomplete': 'address-line1'}))
    city = forms.ChoiceField(label='City', widget=forms.Select(
        attrs={'class': 'state_select'}))
    phone = forms.CharField(label='Phone', widget=forms.TextInput(
        attrs={'class': 'input-text', 'placeholder': _('Phone'), 'autocomplete': 'tel'}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(
        attrs={'class': 'input-text', 'placeholder': _('Email'), 'autocomplete': 'email username'}))
    notes = forms.CharField(label='Notes', widget=forms.Textarea(
        attrs={'class': 'input-text', 'placeholder': _('Notes about your order, e.g. special notes for delivery.')}))
    
    class Meta:
        model = Order
        fields = ("first_name", "last_name", "address", "email", "city", "phone", "notes")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        cities = json.loads(requests.get(url, headers={
            'X-Parse-Application-Id': 'gJ1k7hOymzwNd0uAzWEquCYG7pI53yGaGwzxRdPi', 
            'X-Parse-Master-Key': '0uAjGdZmuqtoiTpbFTiMj1jpMNmr0lWhREtyyCjM'
        }).content.decode('utf-8'))

        self.fields['city'].choices = []