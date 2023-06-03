import uuid
from datetime import datetime

from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from simple_history.models import HistoricalRecords


def service_cover_image_path(instance, filename):
    return f"services/{slugify(instance.name)}-{filename}"


class LanguageField(models.CharField):
    description = _("Language field")

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 2
        kwargs['choices'] = settings.LANGUAGES
        kwargs['default'] = settings.LANGUAGE_CODE
        super().__init__(*args, **kwargs)


class Service(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    language = LanguageField()
    cover_image = models.ImageField(upload_to=service_cover_image_path)
    last_modified_by = models.ForeignKey(
        get_user_model(), on_delete=models.SET_NULL, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

    @property
    def last_modified_by_name(self):
        return str(self.last_modified_by)

    @property
    def language_display_value(self):
        return self.get_language_display

    @property
    def created_date(self):
        return datetime.fromisoformat(str(self.created_at)).strftime("%d.%m.%Y %H:%M")

    @property
    def updated_date(self):
        return datetime.fromisoformat(str(self.updated_at)).strftime("%d.%m.%Y %H:%M")
