
from checkout.utils import getCities
from django.utils.translation import gettext_lazy as _
from orders.models import Order
from rest_framework import serializers


class CheckoutSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(max_length=255, label=_('First Name'), error_messages={'required': _('Please enter your first name')})
    last_name = serializers.CharField(label=_('Last Name'), error_messages={'required': _('Please enter your last name')})
    address = serializers.CharField(label=_('House number and street name'), error_messages={'required': _('Please enter your address')})
    city = serializers.CharField(label=_('City'), error_messages={'required': _('Please select a city')})
    phone = serializers.RegexField(regex=r'^\+?1?\d{12}$', label=_('Phone'), 
                                   error_messages={'required': _('Please enter your phone number'),
                                                   'regex': _('Please enter your phone in correct format')})
    email = serializers.EmailField(label=_('Email'), allow_blank=True, error_messages={'email': _('Please enter a valid email address')})
    notes = serializers.CharField(label=_('Notes'), allow_blank=True)
    
    class Meta:
        model = Order
        fields = ('first_name', 'last_name', 'address', 'city', 'phone', 'email', 'notes')

    def validate_city(self, value):
        cities = getCities()
        if value not in cities:
            raise serializers.ValidationError(_('Invalid city'))
        return value
    
    def create(self, validated_data):
        return Order(**validated_data)

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.address = validated_data.get('address', instance.address)
        instance.city = validated_data.get('city', instance.city)
        instance.email = validated_data.get('email', instance.email)
        instance.phone = validated_data.get('phone', instance.phone)
        instance.notes = validated_data.get('notes', instance.notes)
        return instance