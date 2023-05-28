import uuid
from datetime import datetime

from ckeditor_uploader import fields as ckeditorFields
from django import urls
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from django.template.defaultfilters import slugify


class RichTextEditorField(ckeditorFields.RichTextUploadingField):
    def __init__(self, *args, **kwargs):
        kwargs['null'] = True
        kwargs['blank'] = True
        super().__init__(*args, **kwargs)


def post_cover_image_path(instance, filename):
    return f"posts/{instance.slug}-{filename}"


class Post(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    cover_image = models.ImageField(upload_to=post_cover_image_path)
    description = RichTextEditorField()
    last_modified_by = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, blank=True, null=True)
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
        return datetime.fromisoformat(str(self.created_at)).strftime("%d.%m.%Y %H:%M")
    
    @property
    def updated_date(self):
        return datetime.fromisoformat(str(self.updated_at)).strftime("%d.%m.%Y %H:%M")

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title) + f"{uuid.uuid4()}"
        return super().save(*args, **kwargs)
