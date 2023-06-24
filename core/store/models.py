import os
import shutil
from datetime import datetime, timezone

from ckeditor_uploader import fields as ckeditorFields
from django.conf import settings
from django.contrib.auth import get_user_model
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
    last_modified_by = models.ForeignKey(
        get_user_model(), on_delete=models.SET_NULL, blank=True, null=True)
    parent = TreeForeignKey("self", on_delete=models.PROTECT,
                            related_name="children", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

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

    @property
    def last_modified_by_name(self):
        return str(self.last_modified_by)

    @property
    def created_date(self):
        return datetime.fromisoformat(str(self.created_at)).replace(tzinfo=timezone.utc).astimezone().strftime("%d.%m.%Y %H:%M")

    @property
    def updated_date(self):
        return datetime.fromisoformat(str(self.updated_at)).replace(tzinfo=timezone.utc).astimezone().strftime("%d.%m.%Y %H:%M")


class ProductQuerySet(models.QuerySet):
    def list_queryset(self):
        return self.select_related('category').prefetch_related(
            Prefetch('product_image', queryset=ProductImage.objects.filter(
                is_feature=True), to_attr='image_feature'),
        )

    def detail_queryset(self):
        return self.select_related('category').prefetch_related(
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


default_product_image_path: str = f"{settings.STATIC_URL}images/main/products/default.png"


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
    in_stock = models.BooleanField(default=True)
    maximum_purchase_units = models.IntegerField(
        default=10, validators=[MinValueValidator(0), MaxValueValidator(100)])
    last_modified_by = models.ForeignKey(
        get_user_model(), on_delete=models.SET_NULL, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False,)
    updated_at = models.DateTimeField(auto_now=True)

    products = ProductManager()
    objects = models.Manager()

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name

    @property
    def in_stock_display_value(self):
        return _('In Stock') if self.in_stock else _('Not in Stock')

    @property
    def get_image_feature(self):
        return self.image_feature[0].image.url if self.image_feature else f"{default_product_image_path}"

    @property
    def is_active_display_value(self):
        return _('Active') if self.is_active else _('Not Active')

    @property
    def created_date(self):
        return datetime.fromisoformat(str(self.created_at)).replace(tzinfo=timezone.utc).astimezone().strftime("%d.%m.%Y %H:%M")

    @property
    def updated_date(self):
        return datetime.fromisoformat(str(self.updated_at)).replace(tzinfo=timezone.utc).astimezone().strftime("%d.%m.%Y %H:%M")

    @property
    def last_modified_by_name(self):
        return str(self.last_modified_by)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        self.discount_price = self.regular_price - \
            (self.regular_price * self.discount / 100)
        return super().save(*args, **kwargs)


@receiver(post_delete, sender=Product)
def on_product_delete(sender, instance, *args, **kwargs):
    shutil.rmtree(os.path.join(settings.MEDIA_URL,
                  f"products/{instance.id}"), ignore_errors=False)


def product_image_path(instance, filename):
    return f"products/{instance.product.id}/{filename}"


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="product_image")
    image = models.ImageField(
        upload_to=product_image_path, default=f"{default_product_image_path}")
    is_feature = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-is_feature', )
