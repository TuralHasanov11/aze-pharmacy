import os
import shutil

from ckeditor_uploader import fields as ckeditorFields
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import Prefetch
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.template.defaultfilters import slugify
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from mptt.models import MPTTModel, TreeForeignKey


class Category(MPTTModel):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True)
    parent = TreeForeignKey("self", on_delete=models.PROTECT,
                            related_name="children", null=True, blank=True)

    class MPTTMeta:
        order_insertion_by = ["name"]

    class Meta:
        ordering = ["name"]
        verbose_name_plural = _("categories")

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("store:category-products", kwargs={"category_slug": self.slug})


class ProductQuerySet(models.QuerySet):
    def list_queryset(self):
        return self.select_related('category').prefetch_related(
            Prefetch('product_image', queryset=ProductImage.objects.filter(
                is_feature=True), to_attr='image_feature'),
        )

    def detail_queryset(self):
        return self.select_related('category', 'product_stock').prefetch_related(
            Prefetch('product_image', queryset=ProductImage.objects.filter(
                is_feature=True), to_attr='image_feature'),
            Prefetch('product_image', to_attr='images')
        )


class ProductManager(models.Manager):
    def get_queryset(self):
        return ProductQuerySet(self.model, using=self._db).order_by('-created_at').filter(is_active=True)

    def list_queryset(self):
        return self.get_queryset().list_queryset()

    def detail_queryset(self):
        return self.get_queryset().detail_queryset()


class RichTextEditorField(ckeditorFields.RichTextUploadingField):
    def __init__(self, *args, **kwargs):
        kwargs['null'] = True
        kwargs['blank'] = True
        super().__init__(*args, **kwargs)


class Product(models.Model):
    slug = models.SlugField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    sku = models.CharField(max_length=10, unique=True, null=True)
    description = RichTextEditorField()
    category = models.ForeignKey(
        Category, related_name="product_category", on_delete=models.SET_NULL, null=True, blank=True)
    is_active = models.BooleanField(default=False)
    regular_price = models.DecimalField(max_digits=6, decimal_places=2)
    discount = models.IntegerField(
        default=0, blank=True, validators=[MaxValueValidator(99), MinValueValidator(0)])
    discount_price = models.DecimalField(
        default=0, blank=True, max_digits=6, decimal_places=2)
    weight = models.FloatField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False,)
    updated_at = models.DateTimeField(auto_now=True)

    products = ProductManager()
    objects = models.Manager()

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)


@receiver(post_delete, sender=Product)
def on_product_delete(sender, instance, *args, **kwargs):
    shutil.rmtree(os.path.join(settings.MEDIA_ROOT,
                  f"products/{instance.id}"), ignore_errors=False)


def product_image_path(instance, filename):
    return f"products/{instance.product.id}/{filename}"


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="product_image")
    image = models.ImageField(upload_to=product_image_path)
    is_feature = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-is_feature', )


class Stock(models.Model):
    product = models.OneToOneField(
        Product, related_name="product_stock", on_delete=models.CASCADE) 
    units = models.IntegerField(default=0, validators=[MinValueValidator(0)])
