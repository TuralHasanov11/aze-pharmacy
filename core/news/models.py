import uuid
from datetime import datetime, timezone

from ckeditor_uploader import fields as ckeditorFields
from django import urls
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from django.template.defaultfilters import slugify
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


def post_cover_image_path(instance, filename):
    return f"posts/{instance.slug}-{filename}"


class Post(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    cover_image = models.ImageField(upload_to=post_cover_image_path)
    description = RichTextEditorField()
    last_modified_by = models.ForeignKey(
        get_user_model(), on_delete=models.SET_NULL, blank=True, null=True)
    language = LanguageField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return urls.reverse("news:detail", kwargs={"slug": self.slug})

    @property
    def created_date(self):
        return datetime.fromisoformat(str(self.created_at)).replace(tzinfo=timezone.utc).astimezone().strftime("%d.%m.%Y %H:%M")

    @property
    def updated_date(self):
        return datetime.fromisoformat(str(self.updated_at)).replace(tzinfo=timezone.utc).astimezone().strftime("%d.%m.%Y %H:%M")

    @property
    def last_modified_by_name(self):
        return str(self.last_modified_by)
    
    @property
    def language_display_value(self):
        return self.get_language_display

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title) + f"{uuid.uuid4()}"
        return super().save(*args, **kwargs)
