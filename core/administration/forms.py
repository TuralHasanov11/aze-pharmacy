from ckeditor_uploader import widgets as ckeditor_widgets
from django import forms
from django.contrib.auth import forms as auth_forms
from django.contrib.auth import get_user_model
from django.contrib.auth import models as auth_models
from django.contrib.auth.forms import UserCreationForm
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
    description = forms.CharField(
        label=_("Description"), widget=ckeditor_widgets.CKEditorUploadingWidget())

    class Meta:
        model = Post
        fields = ('title', 'cover_image', 'description')


class UserLoginForm(auth_forms.AuthenticationForm):
    username = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control mb-3', 'placeholder': 'Email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control','placeholder': 'Password',}))
    
    def confirm_login_allowed(self, user):
        pass

class UserCreateForm(UserCreationForm):
    username = forms.CharField(label='Username', max_length=255, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': _('Username')}))
    first_name = forms.CharField(label='First Name', max_length=255, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': _('First Name')}))
    last_name = forms.CharField(label='Last Name', max_length=255, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': _('Last Name')}))
    email = forms.EmailField(label='Email', max_length=255, widget=forms.EmailInput(
        attrs={'class': 'form-control', 'placeholder': _('Email')}))
    role = forms.ChoiceField(label='Role', choices=get_user_model().Role.choices, widget=forms.Select(
        attrs={'class': 'form-select'}), initial=get_user_model().Role.STAFF)
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': _('Password')}))
    password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': _('Password Confirm')}))

    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'role', 'first_name', 'last_name', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data['email']
        if get_user_model().objects.filter(email=email).exists():
            raise forms.ValidationError('Please use another Email, that is already taken')
        return email
    
    def save(self, commit=True):
        user = super().save(commit)
        group = auth_models.Group.objects.get(name=user.get_role_display())
        user.groups.add(group)
        return user
    


class UserUpdateForm(forms.ModelForm):
    username = forms.CharField(label='Username', max_length=255, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': _('Username')}))
    first_name = forms.CharField(label='First Name', max_length=255, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': _('First Name')}))
    last_name = forms.CharField(label='Last Name', max_length=255, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': _('Last Name')}))
    email = forms.EmailField(label='Email', max_length=255, widget=forms.EmailInput(
        attrs={'class': 'form-control', 'placeholder': _('Email')}))
    role = forms.ChoiceField(label='Role', choices=get_user_model().Role.choices, widget=forms.Select(
        attrs={'class': 'form-select'}))

    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'role', 'first_name', 'last_name')

    def save(self, commit=True):
        user = super().save(commit)
        group = auth_models.Group.objects.get(name=user.get_role_display())
        current_group = self.instance.groups.filter(name=user.get_role_display())
        if not current_group:
            user.groups.clear()
            user.groups.add(group)
        return user


class PasswordChangeForm(auth_forms.PasswordChangeForm):
    old_password = forms.CharField(label='Current Password', widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': _('Current Password')}))
    new_password1 = forms.CharField(label='New Password', widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': _('New Password')}))
    new_password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': _('Confirm Password')}))