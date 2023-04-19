from django import forms
from django.utils.translation import gettext_lazy as _


class ContactForm(forms.Form):
    SUBJECT_CHOICES =(
        (_("Delivery & Orders"), _("Delivery & Orders")),
        (_("Wholesale & Returns"), _("Wholesale & Returns")),
        (_("Other"), _("Digər")),
    )
    
    name = forms.CharField(label=_('Full Name'), widget=forms.TextInput(
        attrs={'class': 'wpcf7-form-control wpcf7-text wpcf7-validates-as-required', 'placeholder': _('Full Name')}), required=True)
    email = forms.EmailField(label=_('Email Address'), widget=forms.EmailInput(
        attrs={'class': 'wpcf7-form-control wpcf7-text wpcf7-email wpcf7-validates-as-required wpcf7-validates-as-email', 
               'placeholder': _('Email Address')}), required=True)
    subject = forms.ChoiceField(label=_('Subject'), choices=SUBJECT_CHOICES, widget=forms.Select(
        attrs={'class': 'wpcf7-form-control wpcf7-select wpcf7-validates-as-required form-select', 'placeholder': _('Subject')}), required=True)
    message = forms.CharField(label=_('Message'), widget=forms.Textarea(
        attrs={'class': 'wpcf7-form-control wpcf7-textarea', 'placeholder': _('Message'), 'cols': 40, 'rows': 10}), required=True)




