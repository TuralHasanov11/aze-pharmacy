from django.db.models import Prefetch
from django.http import HttpRequest
from django.shortcuts import render
from django.views.decorators.http import require_GET
from django.views.generic.list import ListView
from main.models import Company
from news.models import Post
from store.models import Product, ProductImage


@require_GET
def index(request: HttpRequest):
    posts = Post.objects.all()[:5]
    companies = Company.objects.all()
    products = Product.products.all().select_related('category').prefetch_related(
                Prefetch('product_image', queryset=ProductImage.objects.filter(is_feature=True), to_attr='image_feature'),
            )
    return render(request, 'main/index.html', context={"posts": posts, "companies": companies, "products": products})


@require_GET
def contact(request: HttpRequest):
    return render(request, 'main/contact.html')


@require_GET
def about(request: HttpRequest):
    return render(request, 'main/about.html')


class CareerListView(ListView):
    model = Company
    template_name = "main/career.html"
    context_object_name = "companies"
