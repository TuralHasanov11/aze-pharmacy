from ckeditor_uploader import fields as ckeditorFields
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _


class RichTextEditorField(ckeditorFields.RichTextUploadingField):
    def __init__(self, *args, **kwargs):
        kwargs['null'] = True
        kwargs['blank'] = True
        super().__init__(*args, **kwargs)


class LanguageField(models.CharField):
    description = _("Language field")
    
    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 2
        kwargs['choices'] = settings.LANGUAGES
        kwargs['default'] = settings.LANGUAGE_CODE
        super().__init__(*args, **kwargs)


def company_cover_image_path(instance, filename):
    return f"companies/{slugify(instance.name)}-{filename}"


class Company(models.Model):
    name = models.CharField(max_length=255, unique=True)
    link = models.URLField()
    cover_image = models.ImageField(upload_to=company_cover_image_path)
    last_modified_by = models.ForeignKey(
        get_user_model(), on_delete=models.SET_NULL, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "companies"

    def __str__(self):
        return self.name
    
    @property
    def last_modified_by_name(self):
        return str(self.last_modified_by)


class SiteInfo(models.Model):
    phone = models.CharField(max_length=20,  null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    facebook_link = models.URLField(null=True, blank=True)
    twitter_link = models.URLField(null=True, blank=True)
    instagram_link = models.URLField(null=True, blank=True)
    youtube_link = models.URLField(null=True, blank=True)
    tiktok_link = models.URLField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    banner_image = models.ImageField(upload_to="site/", null=True, blank=True, default="site/banner_default.jpg")
    breadcrumb_image = models.ImageField(upload_to="site/", null=True, blank=True, default="site/breadcrumb_default.jpg")
    about_image = models.ImageField(upload_to="site/", null=True, blank=True, default="site/about_image_default.jpg")
    last_modified_by = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, blank=True, null=True)

    class Meta:
        verbose_name_plural = "Site Infos"

    def __str__(self):
        return f'Site Info - {self.created_at}'
    
    @property
    def last_modified_by_name(self):
        return str(self.last_modified_by)


class SiteText(models.Model):
    language = LanguageField()
    about = models.TextField(null=True, blank=True)
    return_policy = RichTextEditorField()
    privacy_policy = RichTextEditorField()
    terms_and_conditions = RichTextEditorField()
    last_modified_by = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Site Texts"

    def __str__(self):
        return f'Site Text - {self.language}'
    
    @property
    def last_modified_by_name(self):
        return str(self.last_modified_by)
    

class Question(models.Model):
    language = LanguageField()
    question = models.TextField()
    answer = RichTextEditorField()
    last_modified_by = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.question
    
    @property
    def last_modified_by_name(self):
        return str(self.last_modified_by)
    

