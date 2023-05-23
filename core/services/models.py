from django.db import models
from django.utils.text import slugify


def service_cover_image_path(instance, filename):
    return f"services/{slugify(instance.name)}-{filename}"


class Service(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    cover_image = models.ImageField(upload_to=service_cover_image_path)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name 
    