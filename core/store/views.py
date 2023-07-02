from django.contrib.postgres.search import (SearchQuery, SearchRank,
                                            SearchVector)
from django.core import paginator
from django.http import HttpRequest
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.decorators.http import require_GET
from store.models import Category, Product

orderingContainer = [
    {'name': _('Name'), 'value': 'name'},
    {'name': _('Latest'), 'value': '-created_at'},
    {'name': _('Price low to high'), 'value': 'regular_price'},
    {'name': _('Price high to low'), 'value': '-regular_price'},
]


@require_GET
def products(request: HttpRequest):
    categories = Category.objects.add_related_count(Category.objects.all(), Product,
                                                    'category', 'products_count',
                                                    cumulative=True).all()
    selectedOrderByValue = request.GET.get('order_by', 'name')
    search = request.GET.get('search', None)

    if search:
        searchQuery = SearchQuery(search)
        searchVector = SearchVector(
            "name", "description", "category__name", "regular_price", "discount", "discount_price")
        productsQueryset = Product.products.list_queryset().annotate(
            search=searchVector, rank=SearchRank(searchVector, searchQuery)
        ).filter(search=searchQuery).order_by("rank", selectedOrderByValue)
    else:
        productsQueryset = Product.products.list_queryset().order_by(selectedOrderByValue)

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
    categories = Category.objects.add_related_count(Category.objects.all(), Product,
                                                    'category', 'products_count',
                                                    cumulative=True).all()
    category = Category.objects.get(slug=category_slug)
    categoryFamily = category.get_descendants(include_self=True)
    productsQueryset = Product.products.list_queryset().filter(
        category__in=[cat.id for cat in categoryFamily]).order_by(request.GET.get('sort_by', 'name'))
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
        product = Product.products.detail_queryset().get(
            slug=product_slug, category__slug=category_slug)
        categoryFamily = product.category.get_descendants(include_self=True)
        relatedProducts = Product.products.list_queryset().filter(
            category__in=[cat.id for cat in categoryFamily]).exclude(slug=product_slug).order_by(request.GET.get('sort_by', 'name'))[:4]

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
