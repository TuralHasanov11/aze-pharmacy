from django.contrib.auth import get_user_model
from django.db import models
from django.utils.text import slugify


def service_cover_image_path(instance, filename):
    return f"services/{slugify(instance.name)}-{filename}"


class Service(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
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
