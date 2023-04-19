from django.core import paginator
from django.db.models import Count, Prefetch
from django.http import HttpRequest
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.decorators.http import require_GET
from store.models import Category, Product, ProductImage

orderingContainer = [
    {'name': 'Name', 'value': 'name'}, 
    {'name': 'Latest', 'value': '-created_at'}, 
    {'name': 'Price low to high', 'value': 'regular_price'}, 
    {'name': 'Price high to low', 'value': '-regular_price'},  
]


@require_GET
def products(request: HttpRequest):
    categories = Category.objects.annotate(products_count=Count("product_category")).all()
    selectedOrderByValue = request.GET.get('order_by', 'name')
    products_queryset = Product.products.all().select_related('category').prefetch_related(
                Prefetch('product_image', queryset=ProductImage.objects.filter(is_feature=True), to_attr='image_feature'),
            ).order_by(selectedOrderByValue)
    pagination = paginator.Paginator(products_queryset, 1)
    pageNumber = request.GET.get('page')
    products = pagination.get_page(pageNumber)
    return render(request, 'store/products/index.html', context={
            "products": products, 
            "categories": categories,
            "orderingContainer": orderingContainer,
            "selectedOrderByValue": selectedOrderByValue
        })


@require_GET
def categoryProducts(request: HttpRequest, category_slug: str):
    selectedOrderByValue = request.GET.get('order_by', 'name')
    categories = Category.objects.annotate(products_count=Count("product_category")).all()
    category = Category.objects.get(slug=category_slug)
    products_queryset = Product.products.filter(category__slug=category_slug).select_related('category').prefetch_related(
                Prefetch('product_image', queryset=ProductImage.objects.filter(is_feature=True), to_attr='image_feature'),
            ).order_by(request.GET.get('sort_by', 'name'))
    pagination = paginator.Paginator(products_queryset, 1)
    pageNumber = request.GET.get('page')
    products = pagination.get_page(pageNumber)
    breadcrumb = [
        {"route": reverse("store:products"), "title": _("Products")},
    ]
    return render(request, 'store/products/index.html', context={
            "products": products, 
            "category": category, 
            "categories": categories,
            "orderingContainer": orderingContainer,
            "selectedOrderByValue": selectedOrderByValue,
            "breadcrumb": breadcrumb,
        })


@require_GET
def productDetail(request: HttpRequest, category_slug: str, product_slug: str):
    try:
        product = Product.products.select_related('category', 'product_stock').prefetch_related(
                    Prefetch('product_image', queryset=ProductImage.objects.filter(is_feature=True), to_attr='image_feature'),
                    Prefetch('product_image', to_attr='images')
                ).get(slug=product_slug, category__slug=category_slug)
        breadcrumb = [
            {"route": reverse("store:products"), "title": _("Products")},
            {"route": reverse("store:category-products", kwargs={"category_slug":product.category.slug}), "title": product.category.name}
        ]
    except Product.DoesNotExist:
        return redirect('store:products')
    return render(request, 'store/products/detail.html', context={"product": product, "breadcrumb": breadcrumb})
