from django import template
from django.utils.translation import gettext_lazy as _

register = template.Library()


@register.filter
def convert_weight(value):
    if value and value > 1000:
        return str(round(float(value/1000), 1)) + " " + _("kilograms")
    return str(int(value)) + " " + _("grams")
