import datetime

from bootstrap_datepicker_plus.widgets import DatePickerInput
from ckeditor_uploader import widgets as ckeditor_widgets
from django import forms
from django.conf import settings
from django.contrib.auth import forms as auth_forms
from django.contrib.auth import get_user_model
from django.contrib.auth import models as auth_models
from django.contrib.auth import password_validation
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from library.models import Document
from main.models import Company, Question, SiteInfo, SiteText
from mptt.forms import TreeNodeChoiceField
from news.models import Post
from orders.models import Order, OrderDelivery
from services.models import Service
from store.models import Category, Product, ProductImage


class ServiceForm(forms.ModelForm):
    name = forms.CharField(label=_('Name'), widget=forms.TextInput(
        attrs={'class': 'form-control form-control-sm', 'placeholder': _('Name'), 'title': _('Please enter name'), }))
    cover_image = forms.ImageField(label=_("Cover Image"), widget=forms.ClearableFileInput(
        attrs={'multiple': False, 'class': 'form-control form-control-sm', 'title': _('Please upload image'), }))
    description = forms.CharField(label=_('Description'), widget=forms.Textarea(
        attrs={'class': 'form-control form-control-sm', 'placeholder': _('Description'), 'title': _('Please enter description'), }), required=False)
    language = forms.ChoiceField(label=_("Language"), widget=forms.Select(
        attrs={"class": "form-select form-select-sm",
               'title': _('Please select language')}), choices=settings.LANGUAGES)

    class Meta:
        model = Service
        fields = ('name', 'cover_image', 'description', 'language')

    def __init__(self, *args, **kwargs):
        if 'last_modified_by' in kwargs:
            self.last_modified_by = kwargs.pop('last_modified_by')
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        instance = super().save(commit)
        instance.last_modified_by = self.last_modified_by
        instance.save()
        return instance


class CategoryForm(forms.ModelForm):
    name = forms.CharField(label=_('Name'), widget=forms.TextInput(
        attrs={'class': 'form-control form-control-sm', 'placeholder': _('Name'), 'title': _('Please enter name')}))
    parent = TreeNodeChoiceField(label=_('Parent'),
                                 queryset=Category.objects.all(), required=False)

    class Meta:
        model = Category
        fields = ('name', 'parent')

    def __init__(self, *args, **kwargs):
        if 'last_modified_by' in kwargs:
            self.last_modified_by = kwargs.pop('last_modified_by')
        super().__init__(*args, **kwargs)
        self.fields["parent"].widget.attrs.update(
            {"class": "form-select form-select-sm"})

    def save(self, commit=True):
        instance = super().save(commit)
        instance.last_modified_by = self.last_modified_by
        instance.save()
        return instance


class DocumentForm(forms.ModelForm):
    name = forms.CharField(label=_('Name'), widget=forms.TextInput(
        attrs={'class': 'form-control form-control-sm', 'placeholder': _('Name'), 'title': _('Please enter name')}))
    file = forms.FileField(label=_("File"), widget=forms.ClearableFileInput(
        attrs={'multiple': False, 'class': 'form-control form-control-sm', 'title': _('Please upload file')}))

    class Meta:
        model = Document
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        if 'last_modified_by' in kwargs:
            self.last_modified_by = kwargs.pop('last_modified_by')
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        instance = super().save(commit)
        instance.last_modified_by = self.last_modified_by
        instance.save()
        return instance


class CompanyForm(forms.ModelForm):
    name = forms.CharField(label=_('Name'), widget=forms.TextInput(
        attrs={'class': 'form-control form-control-sm', 'placeholder': _('Name'), 'title': _('Please enter name')}))
    link = forms.URLField(label=_('Link'), widget=forms.URLInput(
        attrs={'class': 'form-control form-control-sm', 'placeholder': _('Link'), 'title': _('Please enter link')}))
    cover_image = forms.ImageField(label=_("Cover Image"), widget=forms.ClearableFileInput(
        attrs={'multiple': False, 'class': 'form-control form-control-sm', 'title': _('Please upload cover image')}))

    class Meta:
        model = Company
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        if 'last_modified_by' in kwargs:
            self.last_modified_by = kwargs.pop('last_modified_by')
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        instance = super().save(commit)
        instance.last_modified_by = self.last_modified_by
        instance.save()
        return instance


class PostForm(forms.ModelForm):
    title = forms.CharField(max_length=255, label=_('Title'), widget=forms.TextInput(
        attrs={'class': 'form-control form-control-sm', 'placeholder': _('Title'), 'title': _('Please enter title')}))
    cover_image = forms.ImageField(label=_("Cover Image"), widget=forms.ClearableFileInput(
        attrs={'multiple': False, 'class': 'form-control form-control-sm', 'title': _('Please upload cover image')}))
    description = forms.CharField(
        label=_("Description"), widget=ckeditor_widgets.CKEditorUploadingWidget())
    language = forms.ChoiceField(label=_("Language"), widget=forms.Select(
        attrs={"class": "form-select form-select-sm",
               'title': _('Please select language')}), choices=settings.LANGUAGES)

    class Meta:
        model = Post
        fields = ('title', 'cover_image', 'description', 'last_modified_by', 'language')

    def __init__(self, *args, **kwargs):
        if 'last_modified_by' in kwargs:
            self.last_modified_by = kwargs.pop('last_modified_by')
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        instance = super().save(commit)
        instance.last_modified_by = self.last_modified_by
        instance.save()
        return instance


class UserLoginForm(auth_forms.AuthenticationForm):
    username = forms.EmailField(label=_('Email'), widget=forms.EmailInput(
        attrs={'class': 'form-control mb-3 form-control-sm', 'placeholder': 'Email', 'title': _('Please enter email')}))
    password = forms.CharField(label=_('Password'), widget=forms.PasswordInput(
        attrs={'class': 'form-control form-control-sm', 'placeholder': 'Password', 'title': _('Please enter password')}))

    def confirm_login_allowed(self, user):
        pass


class UserCreateForm(UserCreationForm):
    username = forms.CharField(label=_('Username'), max_length=255, widget=forms.TextInput(
        attrs={'class': 'form-control form-control-sm', 'placeholder': _('Username'), 'title': _('Please enter username')}))
    first_name = forms.CharField(label=_('First Name'), max_length=255, widget=forms.TextInput(
        attrs={'class': 'form-control form-control-sm', 'placeholder': _('First Name'), 'title': _('Please enter first name')}))
    last_name = forms.CharField(label=_('Last Name'), max_length=255, widget=forms.TextInput(
        attrs={'class': 'form-control form-control-sm', 'placeholder': _('Last Name'), 'title': _('Please enter last name')}))
    email = forms.EmailField(label=_('Email'), max_length=255, widget=forms.EmailInput(
        attrs={'class': 'form-control form-control-sm', 'placeholder': _('Email'), 'title': _('Please enter email')}))
    role = forms.ChoiceField(label=_('Role'), choices=get_user_model().Role.choices, widget=forms.Select(
        attrs={'class': 'form-select form-select-sm', 'title': _('Please select role')}), initial=get_user_model().Role.STAFF)
    password1 = forms.CharField(label=_('Password'), widget=forms.PasswordInput(
        attrs={'class': 'form-control form-control-sm', 'placeholder': _('Password'), 'title': _('Please enter password')}))
    password2 = forms.CharField(label=_('Repeat password'), widget=forms.PasswordInput(
        attrs={'class': 'form-control form-control-sm', 'placeholder': _('Password Confirm'), 'title': _('Please confirm password')}))

    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'role', 'first_name',
                  'last_name', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        if 'last_modified_by' in kwargs:
            self.last_modified_by = kwargs.pop('last_modified_by')
        super().__init__(*args, **kwargs)

    def clean_email(self):
        email = self.cleaned_data['email']
        if get_user_model().objects.filter(email=email).exists():
            raise forms.ValidationError(
                'Please use another Email, that is already taken')
        return email

    def save(self, commit=True):
        user = super().save(commit)
        user.last_modified_by = self.last_modified_by
        group = auth_models.Group.objects.get(name=user.get_role_display())
        user.groups.add(group)
        user.save()
        return user


class UserUpdateForm(forms.ModelForm):
    username = forms.CharField(label=_('Username'), max_length=255, widget=forms.TextInput(
        attrs={'class': 'form-control form-control-sm', 'placeholder': _('Username'), 'title': _('Please enter username')}))
    first_name = forms.CharField(label=_('First Name'), max_length=255, widget=forms.TextInput(
        attrs={'class': 'form-control form-control-sm', 'placeholder': _('First Name'), 'title': _('Please enter first name')}))
    last_name = forms.CharField(label=_('Last Name'), max_length=255, widget=forms.TextInput(
        attrs={'class': 'form-control form-control-sm', 'placeholder': _('Last Name'), 'title': _('Please enter last name')}))
    email = forms.EmailField(label=_('Email'), max_length=255, widget=forms.EmailInput(
        attrs={'class': 'form-control form-control-sm', 'placeholder': _('Email'), 'title': _('Please enter email')}))
    role = forms.ChoiceField(label=_('Role'), choices=get_user_model().Role.choices, widget=forms.Select(
        attrs={'class': 'form-select form-select-sm', 'title': _('Please select role')}))

    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'role', 'first_name', 'last_name')

    def __init__(self, *args, **kwargs):
        if 'last_modified_by' in kwargs:
            self.last_modified_by = kwargs.pop('last_modified_by')
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        user = super().save(commit)
        user.last_modified_by = self.last_modified_by
        group = auth_models.Group.objects.get(name=user.role)
        current_group = self.instance.groups.filter(
            name=user.get_role_display())
        if not current_group:
            user.groups.clear()
            user.groups.add(group)
        user.save()
        return user


class PasswordChangeForm(auth_forms.PasswordChangeForm):
    old_password = forms.CharField(label=_('Current Password'), widget=forms.PasswordInput(
        attrs={'class': 'form-control form-control-sm', 'placeholder': _('Current Password'), 'title': _('Please enter old password')}))
    new_password1 = forms.CharField(label=_('New Password'), widget=forms.PasswordInput(
        attrs={'class': 'form-control form-control-sm', 'placeholder': _('New Password'), 'title': _('Please enter new password')}),
        help_text=_("Password should have at least 12 characters"))
    new_password2 = forms.CharField(label=_('Confirm Password'), widget=forms.PasswordInput(
        attrs={'class': 'form-control form-control-sm', 'placeholder': _('Confirm Password'), 'title': _('Please confirm new password')}))


class PasswordResetForm(forms.ModelForm):
    error_messages = {
        "password_mismatch": _("The two password fields didn’t match."),
    }
    new_password1 = forms.CharField(label=_('New Password'), strip=False, widget=forms.PasswordInput(
        attrs={'class': 'form-control form-control-sm', 'placeholder': _('New Password'), 'title': _('Please enter new password')}),
        help_text=_("Password should have at least 12 characters"))
    new_password2 = forms.CharField(label=_('Confirm Password'), strip=False, widget=forms.PasswordInput(
        attrs={'class': 'form-control form-control-sm', 'placeholder': _('Confirm Password'), 'title': _('Please confirm new password')}))
    
    class Meta:
        model = get_user_model()
        fields = ('new_password1', 'new_password2')
    
    def __init__(self, *args, **kwargs):
        self.last_modified_by = kwargs.pop('last_modified_by')
        super().__init__(*args, **kwargs)

    def clean_new_password2(self):
        password1 = self.cleaned_data.get("new_password1")
        password2 = self.cleaned_data.get("new_password2")
        if password1 and password2:
            if password1 != password2:
                raise ValidationError(
                    self.error_messages["password_mismatch"],
                    code="password_mismatch",
                )
        password_validation.validate_password(password2, self.instance)
        return password2

    def save(self, commit=True):
        user = super().save(commit)
        password = self.cleaned_data["new_password1"]
        user.set_password(password)
        user.last_modified_by = self.last_modified_by
        if commit:
            user.save()
        return user
    

class ProductForm(forms.ModelForm):
    name = forms.CharField(label=_('Name'), widget=forms.TextInput(
        attrs={'class': 'form-control form-control-sm', 'placeholder': _('Name'), 'title': _('Please enter name')}))
    sku = forms.IntegerField(label=_('SKU'), widget=forms.NumberInput(
        attrs={'class': 'form-control form-control-sm', 'placeholder': _('SKU'), 'title': _('Please enter SKU')}))
    category = forms.ModelChoiceField(label=_('Category'), widget=forms.Select(
        attrs={'class': 'form-select form-select-sm', 'title': _('Please select category')}), queryset=Category.objects.all())
    regular_price = forms.DecimalField(label=_('Regular Price'), widget=forms.NumberInput(
        attrs={'class': 'form-control form-control-sm', 'placeholder': _('Regular Price'), 'title': _('Please enter regular price')}))
    discount = forms.IntegerField(label=_('Discount'), widget=forms.NumberInput(
        attrs={'class': 'form-control form-control-sm', 'placeholder': _('Discount'), 'title': _('Please enter discount')}),
        initial=0, required=False)
    weight = forms.IntegerField(label=_('Weight'), widget=forms.NumberInput(
        attrs={'class': 'form-control form-control-sm', 'placeholder': _('Weight'), 'title': _('Please enter weight')}),
        initial=0, required=False)
    is_active = forms.BooleanField(label=_('Is Active'), widget=forms.CheckboxInput(
        attrs={'class': 'form-check-input', 'placeholder': _('Is Active')}), required=False, initial=True)
    in_stock = forms.BooleanField(label=_('In Stock'), widget=forms.CheckboxInput(
        attrs={'class': 'form-check-input', 'placeholder': _('In Stock')}), required=False, initial=True)
    maximum_purchase_units = forms.IntegerField(label=_('Maximum Number of Purchase Units'), widget=forms.NumberInput(
        attrs={'class': 'form-control form-control-sm', 'placeholder': _('Maximum Number of Purchase Units'),
               'title': _('Please enter maximum number of purchase units')}),
        initial=Product._meta.get_field('maximum_purchase_units').default)
    description = forms.CharField(
        label=_("Description"), widget=ckeditor_widgets.CKEditorUploadingWidget(), required=False)

    class Meta:
        model = Product
        fields = ('name', 'sku', 'description', 'regular_price', 'in_stock',
                  'discount', 'weight', 'is_active', 'category', 'maximum_purchase_units')

    def __init__(self, *args, **kwargs):
        if 'last_modified_by' in kwargs:
            self.last_modified_by = kwargs.pop('last_modified_by')
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        instance = super().save(commit)
        instance.last_modified_by = self.last_modified_by
        instance.save()
        return instance


class ProductImageForm(forms.ModelForm):
    image = forms.ImageField(label=_('Image'), widget=forms.ClearableFileInput(
        attrs={'class': 'form-control form-control-sm', 'placeholder': _('Image'), 'title': _('Please upload image'),
               'multiple': False}), required=False)
    is_feature = forms.BooleanField(label=_('Is Feature'), widget=forms.CheckboxInput(
        attrs={'class': 'form-check-input'}), required=False)

    class Meta:
        model = ProductImage
        fields = ('image', 'is_feature')


ProductImageFormSet = forms.inlineformset_factory(
    parent_model=Product, model=ProductImage, form=ProductImageForm, can_delete=True)


class SiteInfoForm(forms.ModelForm):
    phone = forms.CharField(label=_('Phone'), widget=forms.TextInput(
        attrs={'class': 'form-control form-control-sm', 'placeholder': _('Phone'), 'title': _('Please enter phone')}))
    address = forms.CharField(label=_('Address'), widget=forms.TextInput(
        attrs={'class': 'form-control form-control-sm', 'placeholder': _('address'), 'title': _('Please enter address')}))
    email = forms.EmailField(label=_('Email'), widget=forms.EmailInput(
        attrs={'class': 'form-control form-control-sm', 'placeholder': _('Email'), 'title': _('Please enter email')}))
    facebook_link = forms.URLField(label=_('Facebook link'), widget=forms.URLInput(
        attrs={'class': 'form-control form-control-sm', 'placeholder': _('Facebook link'), 'title': _('Please enter facebook link')}))
    instagram_link = forms.URLField(label=_('Instagram link'), widget=forms.URLInput(
        attrs={'class': 'form-control form-control-sm', 'placeholder': _('Instagram link'), 'title': _('Please enter instagram link')}))
    youtube_link = forms.URLField(label=_('YouTube link'), widget=forms.URLInput(
        attrs={'class': 'form-control form-control-sm', 'placeholder': _('YouTube link'), 'title': _('Please enter youtube link')}))
    tiktok_link = forms.URLField(label=_('TikTok link'), widget=forms.URLInput(
        attrs={'class': 'form-control form-control-sm', 'placeholder': _('TikTok link'), 'title': _('Please enter tiktok link')}))
    twitter_link = forms.URLField(label=_('Twitter link'), widget=forms.URLInput(
        attrs={'class': 'form-control form-control-sm', 'placeholder': _('Twitter link'), 'title': _('Please enter twitter link')}))
    banner_image = forms.ImageField(label=_('Banner Image'), widget=forms.ClearableFileInput(
        attrs={'class': 'form-control form-control-sm', 'placeholder': _('Banner Image'), 'title': _('Please upload banner image'),
               'multiple': False}), required=False)
    breadcrumb_image = forms.ImageField(label=_('Breadcrumb Image'), widget=forms.ClearableFileInput(
        attrs={'class': 'form-control form-control-sm', 'placeholder': _('Breadcrumb Image'), 'title': _('Please upload breadcrumb image'),
               'multiple': False}), required=False)
    about_image = forms.ImageField(label=_('About Image'), widget=forms.ClearableFileInput(
        attrs={'class': 'form-control form-control-sm', 'placeholder': _('About Image'), 'title': _('Please upload about image'),
               'multiple': False}), required=False)

    class Meta:
        model = SiteInfo
        fields = ['phone', 'address', 'email', 'facebook_link', 'instagram_link', 'youtube_link', 'tiktok_link',
                  'twitter_link', 'banner_image', 'breadcrumb_image', 'about_image']

    def __init__(self, *args, **kwargs):
        if 'last_modified_by' in kwargs:
            self.last_modified_by = kwargs.pop('last_modified_by')
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        instance = super().save(commit)
        instance.last_modified_by = self.last_modified_by
        instance.save()
        return instance


class SiteTextForm(forms.ModelForm):
    language = forms.ChoiceField(label=_("Language"), widget=forms.Select(
        attrs={"class": "form-select form-select-sm", 'readonly': True,
               'title': _('Please select language')}), choices=settings.LANGUAGES, disabled=True)
    about = forms.CharField(label=_('About'), widget=forms.Textarea(
        attrs={'class': 'form-control form-control-sm', 'placeholder': _('About'), 'rows': 25,
               'title': _('Please enter about text')}), required=False)
    return_policy = forms.CharField(
        label=_("Return Policy"), widget=ckeditor_widgets.CKEditorUploadingWidget(), required=False)
    privacy_policy = forms.CharField(
        label=_("Privacy Policy"), widget=ckeditor_widgets.CKEditorUploadingWidget(), required=False)
    terms_and_conditions = forms.CharField(
        label=_("Terms and Conditions"), widget=ckeditor_widgets.CKEditorUploadingWidget(), required=False)
    order_success = forms.CharField(
        label=_("Order Success Text"), widget=ckeditor_widgets.CKEditorUploadingWidget(), required=False)

    class Meta:
        model = SiteText
        fields = ['about', 'language', 'return_policy', 'order_success',
                  'privacy_policy', 'terms_and_conditions']


SiteTextFormSet = forms.modelformset_factory(
    model=SiteText, form=SiteTextForm, max_num=len(settings.LANGUAGES))


class FAQForm(forms.ModelForm):
    language = forms.ChoiceField(label=_("Language"), widget=forms.Select(
        attrs={"class": "form-select form-select-sm", 'title': _('Please select language')}), choices=settings.LANGUAGES)
    question = forms.CharField(label=_('Question'), widget=forms.Textarea(
        attrs={'class': 'form-control form-control-sm', 'placeholder': _('Question'), 'rows': 5, 'title': _('Please enter question')}))
    answer = forms.CharField(
        label=_("Answer"), widget=ckeditor_widgets.CKEditorUploadingWidget(), required=False)

    class Meta:
        model = Question
        fields = ['question', 'answer', 'language']

    def __init__(self, *args, **kwargs):
        if 'last_modified_by' in kwargs:
            self.last_modified_by = kwargs.pop('last_modified_by')
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        instance = super().save(commit)
        instance.last_modified_by = self.last_modified_by
        instance.save()
        return instance


class OrderForm(forms.ModelForm):
    notes = forms.CharField(label=_('Notes'), widget=forms.Textarea(
        attrs={'class': 'form-control form-control-sm', 'placeholder': _('Notes'), 'title': _('Please enter notes')}), required=False)

    class Meta:
        model = Order
        fields = ('notes',)


class OrderDeliveryForm(forms.ModelForm):
    courier_name = forms.CharField(label=_('Courier Name'), widget=forms.TextInput(
        attrs={'class': 'form-control form-control-sm', 'placeholder': _('Courier Name'),
               'title': _('Please enter courier name')}), required=False)
    tracking_number = forms.CharField(label=_('Tracking Number'), widget=forms.TextInput(
        attrs={'class': 'form-control form-control-sm', 'placeholder': _('Tracking Number'),
               'title': _('Please enter tracking number')}), required=False)
    delivery_status = forms.ChoiceField(label=_('Delivery Status'),
                                        choices=OrderDelivery.DeliveryStatus.choices, widget=forms.Select(
        attrs={'class': 'form-control form-control-sm', 'placeholder': _('Delivery Status'),
               'title': _('Please select delivery status')}))
    delivery_date = forms.DateField(label=_('Delivery Date'), widget=DatePickerInput(
        attrs={'class': 'form-control form-control-sm', 'min': datetime.date.today(),
               'title': _('Please enter delivery date')},
        options={"locale": 'az', "format": "DD-MM-YYYY"}), required=False)

    class Meta:
        model = OrderDelivery
        fields = ('courier_name', 'tracking_number',
                  'delivery_status', 'delivery_date')

    STAGES = {
        "PROCESSING": [OrderDelivery.DeliveryStatus.SHIPPED.name, OrderDelivery.DeliveryStatus.CANCELLED.name],
        "SHIPPED": [OrderDelivery.DeliveryStatus.DELIVERED.name, OrderDelivery.DeliveryStatus.FAILED_DELIVERY.name],
        "DELIVERED": [OrderDelivery.DeliveryStatus.RETURNED.name],
        "FAILED_DELIVERY": [OrderDelivery.DeliveryStatus.PROCESSING.name, OrderDelivery.DeliveryStatus.PROCESSING.name],
        "RETURNED": [OrderDelivery.DeliveryStatus.PROCESSING.name],
        "CANCELLED": [],
    }

    def clean_delivery_status(self):
        delivery_status = self.cleaned_data['delivery_status']
        if (self.cleaned_data['delivery_status'] != self.instance.delivery_status
                and str(self.cleaned_data['delivery_status']) not in self.STAGES[self.instance.delivery_status]):
            raise forms.ValidationError(
                _("Delivery Status cannot be changed!"))
        return delivery_status

    def clean_delivery_date(self):
        delivery_date = self.cleaned_data['delivery_date']
        if (self.cleaned_data['delivery_date'] < datetime.date.today()):
            raise forms.ValidationError(
                _("Delivery date can be minimum today"))
        return delivery_date


class OrderRefundForm(forms.ModelForm):
    amount = forms.DecimalField(label=_('Refund Amount'), widget=forms.NumberInput(
        attrs={'class': 'form-control form-control-sm', 'placeholder': _('Refund Amount'),
               'title': _('Please enter refund amount')}),
        help_text=_('Refund Amount should not be greater than remainder of total payment'), required=False)
    reason = forms.CharField(label=_('Reason'), widget=forms.Textarea(
        attrs={'class': 'form-control form-control-sm', 'placeholder': _('Reason'),
               'title': _('Please enter reason')}))
    full_refund = forms.BooleanField(required=False, initial=False, label=_('Full Refund'), widget=forms.CheckboxInput(
        attrs={'class': 'form-check-input', 'placeholder': _('Full Refund')}))

    class Meta:
        model = OrderDelivery
        fields = ('amount', 'reason', 'full_refund')


class ProductFilterForm(forms.Form):
    category = TreeNodeChoiceField(label=_('category'), widget=forms.Select(
        attrs={'class': 'form-select form-select-sm'}), queryset=Category.objects.all(), required=False)
    is_active = forms.BooleanField(label=_('Is Active'), widget=forms.CheckboxInput(
        attrs={'class': 'form-check-input'}), required=False, initial=True)
    in_stock = forms.BooleanField(label=_('In Stock'), widget=forms.CheckboxInput(
        attrs={'class': 'form-check-input'}), required=False, initial=True)