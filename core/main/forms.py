from django import forms
from django.utils.translation import gettext_lazy as _


class ContactForm(forms.Form):
    SUBJECT_CHOICES = (
        (_("Order Status and Tracking"), _("Order Status and Tracking")),
        (_("Returns and Refunds"), _("Returns and Refunds")),
        (_("Shipping and Delivery"), _("Shipping and Delivery")),
        (_("Payment and Billing"), _("Payment and Billing")),
        (_("Product Availability"), _("Product Availability")),
        (_("Website Feedback or Issues"), _("Website Feedback or Issues")),
        (_("Promotions and Discounts"), _("Promotions and Discounts")),
        (_("Collaborations or Partnerships"), _("Collaborations or Partnerships")),
        (_("Privacy and Data Security"), _("Privacy and Data Security")),
        (_("Other"), _("Other")),
    )

    name = forms.CharField(label=_('Full Name'), widget=forms.TextInput(
        attrs={'class': 'wpcf7-form-control wpcf7-text wpcf7-validates-as-required',
               'title': _('Please enter your full name'), 'placeholder': _('Full Name')}),
        error_messages={'required': _('Please enter your full name')}, required=True)
    email = forms.EmailField(label=_('Email Address'), widget=forms.EmailInput(
        attrs={'class': 'wpcf7-form-control wpcf7-text wpcf7-email wpcf7-validates-as-required wpcf7-validates-as-email',
               'title': _('Please enter your email address'), 'placeholder': _('Email Address')}),
        error_messages={'required': _('Please enter your email address')}, required=True)
    subject = forms.ChoiceField(label=_('Subject'), choices=SUBJECT_CHOICES, widget=forms.Select(
        attrs={'class': 'wpcf7-form-control wpcf7-select wpcf7-validates-as-required form-select',
               'placeholder': _('Subject'), 'title': _('Please select a subject')}),
        error_messages={'required': _('Please select a subject')}, required=True)
    message = forms.CharField(label=_('Message'), widget=forms.Textarea(
        attrs={'class': 'wpcf7-form-control wpcf7-textarea', 'placeholder': _('Message'), 'cols': 40, 'rows': 10,
               'title': _('Please enter your message'), }), error_messages={'required': _('Please enter your message')},
        required=True)
