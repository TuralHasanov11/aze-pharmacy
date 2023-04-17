import json
import os

from django import forms
from django.conf import settings
from django.contrib.staticfiles import finders
from django.contrib.staticfiles.storage import staticfiles_storage
from django.core.files import File
from django.utils.translation import gettext_lazy as _
from orders.models import Order


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
        result = finders.find("data/cities.json")
        with open(result, "r", encoding='utf-8') as f:
            citiesFile = File(f)
            cities: list = json.loads(citiesFile.read())
        self.fields['city'].choices = [tuple(item.values()) for item in cities]