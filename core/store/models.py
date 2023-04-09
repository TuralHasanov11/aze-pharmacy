# from decimal import Decimal

from ckeditor_uploader import fields as ckeditorFields
from django import urls
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.template.defaultfilters import slugify
from django.utils.translation import gettext_lazy as _
from mptt.models import MPTTModel, TreeForeignKey


class Category(MPTTModel):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True)
    parent = TreeForeignKey("self", on_delete=models.PROTECT, related_name="children", null=True, blank=True)

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


class ProductManager(models.Manager):
    def get_queryset(self):
        return super(ProductManager, self).get_queryset().filter(is_active=True)


class RichTextEditorField(ckeditorFields.RichTextUploadingField):
    description = _("Rich text editor field")

    def __init__(self, *args, **kwargs):
        kwargs['null'] = True
        kwargs['blank'] = True
        super().__init__(*args, **kwargs) 


class Product(models.Model):
    slug = models.SlugField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    description = RichTextEditorField()
    category = models.ForeignKey(Category, related_name="category", on_delete=models.SET_NULL, null=True, blank=True)
    is_active = models.BooleanField(default=False)
    regular_price = models.DecimalField(max_digits=6, decimal_places=2)
    discount = models.IntegerField(default=0, blank=True, validators=[MaxValueValidator(99)])
    discount_price = models.DecimalField(default=0, blank=True, max_digits=6, decimal_places=2)
    weight = models.FloatField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False,)
    updated_at = models.DateTimeField(auto_now=True)

    products = ProductManager()
    objects = models.Manager()

    class Meta:
        ordering = ('name',)

    def get_absolute_url(self):
        return urls.reverse("store:product_detail", kwargs={"slug": self.slug})
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)
    
    
    
def product_image_path(instance, filename):
    return f"products/{instance.product.slug}/{filename}"


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="product_image")
    image = models.ImageField(upload_to=product_image_path)
    is_feature = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)


class Stock(models.Model):
    product = models.OneToOneField(Product, related_name="product_stock", on_delete=models.CASCADE)
    units = models.IntegerField(default=0)
    units_sold = models.IntegerField(default=0)