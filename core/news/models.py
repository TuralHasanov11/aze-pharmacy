import uuid

from ckeditor_uploader import fields as ckeditorFields
from django import urls
from django.conf import settings
from django.db import models
from django.template.defaultfilters import slugify
from django.utils.translation import gettext_lazy as _


class RichTextEditorField(ckeditorFields.RichTextUploadingField):
    description = _("Rich text editor field")

    def __init__(self, *args, **kwargs):
        kwargs['null'] = True
        kwargs['blank'] = True
        super().__init__(*args, **kwargs)

def post_cover_image_path(instance, filename):
    return f"posts/{instance.slug}/{filename}"

class Post(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    cover_image = models.ImageField(upload_to=post_cover_image_path)
    description = RichTextEditorField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return urls.reverse("news:detail", kwargs={"slug": self.slug})

    @property
    def get_absolute_cover_image_url(self):
        return f"{settings.MEDIA_URL}{self.cover_image.url}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title) + f"{uuid.uuid4()}"
        return super().save(*args, **kwargs)