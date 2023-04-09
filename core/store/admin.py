from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin
from store.models import Category, Product, ProductImage, Stock


@admin.register(Category)
class CategoryAdmin(DraggableMPTTAdmin):
    mptt_indent_field = "name"
    list_display = ('tree_actions', 'indented_title')
    list_display_links = ('indented_title',)
    prepopulated_fields = {'slug': ('name',)}

class ProductImageInline(admin.TabularInline):
    model = ProductImage


class StockInline(admin.StackedInline):
    model = Stock


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [
        StockInline,
        ProductImageInline,
    ]
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ('product', 'units', 'units_sold')


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('product', 'image')