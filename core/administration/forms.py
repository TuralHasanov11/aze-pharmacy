from ckeditor_uploader import widgets as ckeditor_widgets
from django import forms
from django.conf import settings
from django.contrib.auth import forms as auth_forms
from django.contrib.auth import get_user_model
from django.contrib.auth import models as auth_models
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _
from library.models import Document
from main.models import Company, Question, SiteInfo, SiteText
from mptt.forms import TreeNodeChoiceField
from news.models import Post
from services.models import Service
from store.models import Category, Product, ProductImage, Stock


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


class CategoryForm(forms.ModelForm):
    name = forms.CharField(label=_('Name'), widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': _('Name')}))
    parent = TreeNodeChoiceField(
        queryset=Category.objects.all(), required=False)

    class Meta:
        model = Category
        fields = ('name', 'parent')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["parent"].widget.attrs.update({"class": "form-select"})


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
    title = forms.CharField(max_length=255, label=_('Title'), widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': _('Title')}))
    cover_image = forms.ImageField(label=_("Cover Image"), widget=forms.ClearableFileInput(
        attrs={'multiple': False, 'class': 'form-control'}))
    description = forms.CharField(
        label=_("Description"), widget=ckeditor_widgets.CKEditorUploadingWidget())

    class Meta:
        model = Post
        fields = ('title', 'cover_image', 'description')


class UserLoginForm(auth_forms.AuthenticationForm):
    username = forms.EmailField(label=_('Email'), widget=forms.EmailInput(
        attrs={'class': 'form-control mb-3', 'placeholder': 'Email'}))
    password = forms.CharField(label=_('Password'), widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Password', }))

    def confirm_login_allowed(self, user):
        pass


class UserCreateForm(UserCreationForm):
    username = forms.CharField(label=_('Username'), max_length=255, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': _('Username')}))
    first_name = forms.CharField(label=_('First Name'), max_length=255, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': _('First Name')}))
    last_name = forms.CharField(label=_('Last Name'), max_length=255, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': _('Last Name')}))
    email = forms.EmailField(label=_('Email'), max_length=255, widget=forms.EmailInput(
        attrs={'class': 'form-control', 'placeholder': _('Email')}))
    role = forms.ChoiceField(label=_('Role'), choices=get_user_model().Role.choices, widget=forms.Select(
        attrs={'class': 'form-select'}), initial=get_user_model().Role.STAFF)
    password1 = forms.CharField(label=_('Password'), widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': _('Password')}))
    password2 = forms.CharField(label=_('Repeat password'), widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': _('Password Confirm')}))

    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'role', 'first_name',
                  'last_name', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data['email']
        if get_user_model().objects.filter(email=email).exists():
            raise forms.ValidationError(
                'Please use another Email, that is already taken')
        return email

    def save(self, commit=True):
        user = super().save(commit)
        group = auth_models.Group.objects.get(name=user.get_role_display())
        user.groups.add(group)
        return user


class UserUpdateForm(forms.ModelForm):
    username = forms.CharField(label=_('Username'), max_length=255, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': _('Username')}))
    first_name = forms.CharField(label=_('First Name'), max_length=255, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': _('First Name')}))
    last_name = forms.CharField(label=_('Last Name'), max_length=255, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': _('Last Name')}))
    email = forms.EmailField(label=_('Email'), max_length=255, widget=forms.EmailInput(
        attrs={'class': 'form-control', 'placeholder': _('Email')}))
    role = forms.ChoiceField(label=_('Role'), choices=get_user_model().Role.choices, widget=forms.Select(
        attrs={'class': 'form-select'}))

    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'role', 'first_name', 'last_name')

    def save(self, commit=True):
        user = super().save(commit)
        group = auth_models.Group.objects.get(name=user.get_role_display())
        current_group = self.instance.groups.filter(
            name=user.get_role_display())
        if not current_group:
            user.groups.clear()
            user.groups.add(group)
        return user


class PasswordChangeForm(auth_forms.PasswordChangeForm):
    old_password = forms.CharField(label=_('Current Password'), widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': _('Current Password')}))
    new_password1 = forms.CharField(label=_('New Password'), widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': _('New Password')}))
    new_password2 = forms.CharField(label=_('Confirm Password'), widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': _('Confirm Password')}))


class ProductForm(forms.ModelForm):
    name = forms.CharField(label=_('Name'), widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': _('Name')}))
    sku = forms.IntegerField(label=_('SKU'), widget=forms.NumberInput(
        attrs={'class': 'form-control', 'placeholder': _('SKU')}))
    category = forms.ModelChoiceField(label=_('category'), widget=forms.Select(
        attrs={'class': 'form-select'}), queryset=Category.objects.all())
    regular_price = forms.DecimalField(label=_('Regular Price'), widget=forms.NumberInput(
        attrs={'class': 'form-control', 'placeholder': _('Regular Price')}))
    discount = forms.IntegerField(label=_('Discount'), widget=forms.NumberInput(
        attrs={'class': 'form-control', 'placeholder': _('Discount')}), initial=0, required=False)
    weight = forms.IntegerField(label=_('Weight'), widget=forms.NumberInput(
        attrs={'class': 'form-control', 'placeholder': _('Weight')}), initial=0, required=False)
    is_active = forms.BooleanField(label=_('Is Active'), widget=forms.CheckboxInput(
        attrs={'class': 'form-check-input', 'placeholder': _('Is Active')}), required=False)
    description = forms.CharField(
        label=_("Description"), widget=ckeditor_widgets.CKEditorUploadingWidget(), required=False)

    class Meta:
        model = Product
        fields = ('name', 'sku', 'description', 'regular_price',
                  'discount', 'weight', 'is_active', 'category')

    def save(self, commit=True):
        product = super().save(commit)
        product.discount_price = product.regular_price - \
            (product.regular_price * product.discount / 100)
        product.save()
        return product


class StockForm(forms.ModelForm):
    units = forms.IntegerField(label=_('Units'), widget=forms.NumberInput(
        attrs={'class': 'form-control', 'placeholder': _('Units')}), initial=0, required=False)

    class Meta:
        model = Stock
        fields = ('units',)


class ProductImageForm(forms.ModelForm):
    image = forms.ImageField(label=_('Image'), widget=forms.ClearableFileInput(
        attrs={'class': 'form-control', 'placeholder': _('Image'), 'multiple': False}), required=False)
    is_feature = forms.BooleanField(label=_('Is Feature'), widget=forms.CheckboxInput(
        attrs={'class': 'form-check-input'}), required=False)

    class Meta:
        model = Stock
        fields = ('image', 'is_feature')


StockFormSet = forms.inlineformset_factory(
    parent_model=Product, model=Stock, max_num=1, form=StockForm)
ProductImageFormSet = forms.inlineformset_factory(
    parent_model=Product, model=ProductImage, form=ProductImageForm, can_delete=True)


class SiteInfoForm(forms.ModelForm):
    phone = forms.CharField(label=_('Phone'), widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': _('Phone')}))
    address = forms.CharField(label=_('Address'), widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': _('address')}))
    email = forms.EmailField(label=_('Email'), widget=forms.EmailInput(
        attrs={'class': 'form-control', 'placeholder': _('Email')}))
    facebook_link = forms.URLField(label=_('Facebook link'), widget=forms.URLInput(
        attrs={'class': 'form-control', 'placeholder': _('Facebook link')}))
    instagram_link = forms.URLField(label=_('Instagram link'), widget=forms.URLInput(
        attrs={'class': 'form-control', 'placeholder': _('Instagram link')}))
    youtube_link = forms.URLField(label=_('YouTube link'), widget=forms.URLInput(
        attrs={'class': 'form-control', 'placeholder': _('YouTube link')}))
    tiktok_link = forms.URLField(label=_('TikTok link'), widget=forms.URLInput(
        attrs={'class': 'form-control', 'placeholder': _('TikTok link')}))
    twitter_link = forms.URLField(label=_('Twitter link'), widget=forms.URLInput(
        attrs={'class': 'form-control', 'placeholder': _('Twitter link')}))

    class Meta:
        model = SiteInfo
        fields = ['phone', 'address', 'email', 'facebook_link',
                  'instagram_link', 'youtube_link', 'tiktok_link', 'twitter_link']


class SiteTextForm(forms.ModelForm):
    language = forms.ChoiceField(label=_("Language"), widget=forms.Select(
        attrs={"class": "form-select", 'readonly': True}), choices=settings.LANGUAGES)
    about = forms.CharField(label=_('About'), widget=forms.Textarea(
        attrs={'class': 'form-control', 'placeholder': _('About'), 'rows': 25}))
    return_policy = forms.CharField(
        label=_("Return Policy"), widget=ckeditor_widgets.CKEditorUploadingWidget(), required=False)
    privacy_policy = forms.CharField(
        label=_("Privacy Policy"), widget=ckeditor_widgets.CKEditorUploadingWidget(), required=False)
    terms_and_conditions = forms.CharField(
        label=_("Terms and Conditions"), widget=ckeditor_widgets.CKEditorUploadingWidget(), required=False)

    class Meta:
        model = SiteText
        fields = ['about', 'language', 'return_policy',
                  'privacy_policy', 'terms_and_conditions']


class FAQForm(forms.ModelForm):
    language = forms.ChoiceField(label=_("Language"), widget=forms.Select(
        attrs={"class": "form-select", 'readonly': True}), choices=settings.LANGUAGES)
    question = forms.CharField(label=_('Question'), widget=forms.Textarea(
        attrs={'class': 'form-control', 'placeholder': _('Question'), 'rows': 25}))
    answer = forms.CharField(
        label=_("Answer"), widget=ckeditor_widgets.CKEditorUploadingWidget(), required=False)

    class Meta:
        model = Question
        fields = ['question', 'answer', 'language']


SiteTextFormSet = forms.modelformset_factory(
    model=SiteText, form=SiteTextForm, max_num=len(settings.LANGUAGES))
