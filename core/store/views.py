from django.contrib.postgres.search import (SearchQuery, SearchRank,
                                            SearchVector)
from django.core import paginator
from django.db.models import Count, Prefetch
from django.http import HttpRequest
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.decorators.http import require_GET
from store.models import Category, Product, ProductImage

orderingContainer = [
    {'name': _('Name'), 'value': 'name'},
    {'name': _('Latest'), 'value': '-created_at'},
    {'name': _('Price low to high'), 'value': 'regular_price'},
    {'name': _('Price high to low'), 'value': '-regular_price'},
]


@require_GET
def products(request: HttpRequest):
    categories = Category.objects.annotate(
        products_count=Count("product_category")).all().order_by("name")
    selectedOrderByValue = request.GET.get('order_by', 'name')
    search = request.GET.get('search', None)
    
    if search:
        searchQuery = SearchQuery(search)
        searchVector = SearchVector("name", "description", "category__name", "regular_price", "discount", "discount_price")
        productsQueryset = Product.products.annotate(
            search=searchVector, rank=SearchRank(searchVector, searchQuery)
        ).filter(search=searchQuery).select_related('category').prefetch_related(
            Prefetch('product_image', queryset=ProductImage.objects.filter(
                is_feature=True), to_attr='image_feature'),
        ).order_by("rank", selectedOrderByValue)
    else:
        productsQueryset = Product.products.select_related('category').prefetch_related(
            Prefetch('product_image', queryset=ProductImage.objects.filter(
                is_feature=True), to_attr='image_feature'),
        ).order_by(selectedOrderByValue)
    
    pagination = paginator.Paginator(productsQueryset, 20)
    pageNumber = request.GET.get('page')
    products = pagination.get_page(pageNumber)
    breadcrumb = [
        {"title": _("Shop")},
        {"title": _("Home"), "route": reverse("main:index")},
        {"title": _("Products")},
    ]

    return render(request, 'store/products/index.html', context={
        "products": products,
        "categories": categories,
        "orderingContainer": orderingContainer,
        "selectedOrderByValue": selectedOrderByValue,
        'breadcrumb': breadcrumb
    })


@require_GET
def categoryProducts(request: HttpRequest, category_slug: str):
    selectedOrderByValue = request.GET.get('order_by', 'name')
    categories = Category.objects.annotate(
        products_count=Count("product_category")).all().order_by("name")
    category = Category.objects.get(slug=category_slug)
    productsQueryset = Product.products.filter(category__slug=category_slug).select_related('category').prefetch_related(
        Prefetch('product_image', queryset=ProductImage.objects.filter(
            is_feature=True), to_attr='image_feature'),
    ).order_by(request.GET.get('sort_by', 'name'))
    pagination = paginator.Paginator(productsQueryset, 20)
    pageNumber = request.GET.get('page')
    products = pagination.get_page(pageNumber)
    breadcrumb = [
        {"title": _("Shop")},
        {"title": _("Home"), "route": reverse("main:index")},
        {"route": reverse("store:products"), "title": _("Products")},
        {"route": reverse("store:category-products", kwargs={
                              "category_slug": category.slug}), "title": category.name},
        {"title": _("Products")},
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
            Prefetch('product_image', queryset=ProductImage.objects.filter(
                is_feature=True), to_attr='image_feature'),
            Prefetch('product_image', to_attr='images')
        ).get(slug=product_slug, category__slug=category_slug)

        relatedProducts = Product.products.filter(category__slug=product.category.slug).select_related('category').prefetch_related(
            Prefetch('product_image', queryset=ProductImage.objects.filter(
                is_feature=True), to_attr='image_feature'),
        ).order_by(request.GET.get('sort_by', 'name'))[:4]

        breadcrumb = [
            {"title": _("Shop")},
            {"title": _("Home"), "route": reverse("main:index")},
            {"route": reverse("store:products"), "title": _("Products")},
            {"route": reverse("store:category-products", kwargs={
                              "category_slug": product.category.slug}), "title": product.category.name},
            {"title": product.name},
        ]
    except Product.DoesNotExist:
        return redirect('store:products')
    return render(request, 'store/products/detail.html', context={"product": product, "breadcrumb": breadcrumb, "related_products": relatedProducts})
