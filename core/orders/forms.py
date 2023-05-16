import json

from django import forms
from django.contrib.staticfiles import finders
from django.core.files import File
from django.utils.translation import gettext_lazy as _
from orders.models import Order


class OrderForm(forms.ModelForm):
    first_name = forms.CharField(label=_('First Name'), widget=forms.TextInput(
        attrs={'class': 'input-text', 'placeholder': _('First Name'), 'autocomplete': 'given-name',
               'title': _('Please enter your first name'), }))
    last_name = forms.CharField(label=_('Last Name'), widget=forms.TextInput(
        attrs={'class': 'input-text', 'placeholder': _('Last Name'), 'autocomplete': 'family-name', 
               'title': _('Please enter your last name'), }))
    address = forms.CharField(label=_('House number and street name'), widget=forms.TextInput(
        attrs={'class': 'input-text', 'placeholder': _('House number and street name'), 'autocomplete': 'address-line1',
               'title': _('Please enter your address'), }))
    city = forms.ChoiceField(label=_('City'), widget=forms.Select(
        attrs={'class': 'state_select', 'title': _('Please select a city'), }))
    phone = forms.RegexField(regex=r'^\+?1?\d{9,15}$', label=_('Phone'), widget=forms.TextInput(
        attrs={'class': 'input-text phone-input', 'placeholder': _('+xxxxxxxxx'), 'autocomplete': 'tel', 'title': _('Please enter your phone number'), }),
        help_text=_("Phone number must be entered in the format: '+xxxxxxxxx'. Up to 15 digits allowed"))
    email = forms.EmailField(label=_('Email'), widget=forms.EmailInput(
        attrs={'class': 'input-text', 'placeholder': _('Email'), 'autocomplete': 'email username'}), required=False)
    notes = forms.CharField(label=_('Notes'), widget=forms.Textarea(
        attrs={'class': 'input-text', 'placeholder': _('Notes about your order, e.g. special notes for delivery.'),
               'title': _('Please enter your notes'), }), required=False)

    class Meta:
        model = Order
        fields = ("first_name", "last_name", "address",
                  "email", "city", "phone", "notes")
        
    def clean_city(self):
        city = self.cleaned_data['city']
        if (city, city) in self.fields['city'].choices:
            raise forms.ValidationError(_('Invalid city'))
        return city

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        result = finders.find("data/cities.json")
        with open(result, "r", encoding='utf-8') as f:
            citiesFile = File(f)
            cities: list = json.loads(citiesFile.read())
        self.fields['city'].choices = [tuple(item.values()) for item in cities]
