import json

from django.contrib.staticfiles import finders
from django.core.files import File
from django.utils.translation import gettext_lazy as _
from orders.models import Order
from rest_framework import serializers


class OrderSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(max_length=255, label=_('First Name'))
    last_name = serializers.CharField(label=_('Last Name'))
    address = serializers.CharField(label=_('House number and street name'))
    city = serializers.CharField(label=_('City'))
    phone = serializers.RegexField(regex=r'^\+?1?\d{9,15}$', label=_('Phone'))
    email = serializers.EmailField(label=_('Email'), allow_blank=True)
    notes = serializers.CharField(label=_('Notes'), allow_blank=True)
    
    class Meta:
        model = Order

    def validate_city(self, value):
        result = finders.find("data/cities.json")
        with open(result, "r", encoding='utf-8') as f:
            citiesFile = File(f)
            cities: list = [item.values()[0] for item in json.loads(citiesFile.read())]

        if value not in cities:
            raise serializers.ValidationError(_('Invalid city'))
        return value