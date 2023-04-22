
import os

from django.contrib import messages
from django.core.mail import BadHeaderError, send_mail
from django.db.models import Prefetch
from django.http import HttpRequest
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.translation import get_language
from django.views.decorators.http import require_GET, require_http_methods
from django.views.generic.list import ListView
from main.forms import ContactForm
from main.models import Company, SiteInfo, SiteText
from news.models import Post
from store.models import Product, ProductImage


@require_GET
def index(request: HttpRequest):
    posts = Post.objects.all()[:5]
    companies = Company.objects.all()
    products = Product.products.all().select_related('category').prefetch_related(
                Prefetch('product_image', queryset=ProductImage.objects.filter(is_feature=True), to_attr='image_feature'),
            )
    siteText = SiteText.objects.values('about').filter(language=get_language()).first()
    return render(request, 'main/index.html', context={"posts": posts, "companies": companies, "products": products, "about": siteText["about"]})


@require_http_methods(['GET', 'POST'])
def contact(request: HttpRequest):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        siteInfo = SiteInfo.objects.first()
        if form.is_valid():
            data = form.cleaned_data
            try:
                send_mail(data["subject"], data["message"], data["email"], [os.environ.get("COMPANY_EMAIL", "")])
            except BadHeaderError:
                messages.error(request, "Email cannot be sent")
                return render(request, "main/contact.html", {"form": form, 'siteInfo': siteInfo})
            messages.success(request, 'Email was sent successfully!')
            return redirect(reverse("main:contact")+"#contact-form")
        messages.error(request, "Email cannot be sent")
        return render(request, "main/contact.html", {"form": form, 'siteInfo': siteInfo})
    siteInfo = SiteInfo.objects.first()
    form = ContactForm()
    return render(request, 'main/contact.html', {'siteInfo': siteInfo, "form": form})


@require_GET
def about(request: HttpRequest):
    siteText = SiteText.objects.values('about').filter(language=get_language()).first()
    return render(request, 'main/about.html', {'siteText': siteText})


class CareerListView(ListView):
    model = Company
    template_name = "main/career.html"
    context_object_name = "companies"


@require_GET
def search(request: HttpRequest):
    pass