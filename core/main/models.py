from django.conf import settings
from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _


class LanguageField(models.CharField):
    description = _("Language field")
    
    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 2
        kwargs['choices'] = settings.LANGUAGES
        kwargs['default'] = settings.LANGUAGE_CODE
        super().__init__(*args, **kwargs)


def company_cover_image_path(instance, filename):
    return f"companies/{slugify(instance.name)}/{filename}"


class Company(models.Model):
    name = models.CharField(max_length=255, unique=True)
    link = models.URLField()
    cover_image = models.ImageField(upload_to=company_cover_image_path)

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "companies"

    def __str__(self):
        return self.name


class SiteInfo(models.Model):
    phone = models.CharField(max_length=20,  null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    facebook_link = models.URLField(null=True, blank=True)
    twitter_link = models.URLField(null=True, blank=True)
    instagram_link = models.URLField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Site Infos"

    def __str__(self):
        return f'Site Info - {self.created_at}'


class SiteText(models.Model):
    language = LanguageField()
    about = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Site Infos"

    def __str__(self):
        return f'Site Info - {self.created_at}'