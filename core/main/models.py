from django.db import models
from django.utils.text import slugify


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
