from ckeditor_uploader import widgets as ckeditor_widgets
from django import forms
# from django.conf import settings
from django.utils.translation import gettext_lazy as _
from library.models import Document
from main.models import Company
from news.models import Post
from services.models import Service


class ServiceForm(forms.ModelForm):
    name = forms.CharField(label=_('Name'), widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': _('Name')}))
    cover_image = forms.ImageField(label=_("Cover Image"), widget=forms.ClearableFileInput(
        attrs={'multiple': False, 'class': 'form-control'}))
    description = forms.CharField(label=_('Description'), widget=forms.Textarea(
        attrs={'class': 'form-control', 'placeholder': _('Description')}), required=False)

    class Meta:
        model = Service
        fields = '__all__'


class DocumentForm(forms.ModelForm):
    name = forms.CharField(label=_('Name'), widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': _('Name')}))
    file = forms.FileField(label=_("File"), widget=forms.ClearableFileInput(
        attrs={'multiple': False, 'class': 'form-control'}))

    class Meta:
        model = Document
        fields = '__all__'


class CompanyForm(forms.ModelForm):
    name = forms.CharField(label=_('Name'), widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': _('Name')}))
    link = forms.URLField(label=_('Link'), widget=forms.URLInput(
        attrs={'class': 'form-control', 'placeholder': _('Link')}))
    cover_image = forms.ImageField(label=_("Cover Image"), widget=forms.ClearableFileInput(
        attrs={'multiple': False, 'class': 'form-control'}))

    class Meta:
        model = Company
        fields = '__all__'


class PostForm(forms.ModelForm):
    title = forms.CharField(label=_('Title'), widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': _('Title')}))
    cover_image = forms.ImageField(label=_("Cover Image"), widget=forms.ClearableFileInput(
        attrs={'multiple': False, 'class': 'form-control'}))
    description = forms.CharField(label=_("Description"), widget=ckeditor_widgets.CKEditorUploadingWidget())

    class Meta:
        model = Post
        fields = ('title', 'cover_image', 'description')