
import os

from django.contrib import messages
from django.core.mail import BadHeaderError, send_mail
from django.db.models import Count, Prefetch
from django.http import HttpRequest
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.translation import get_language
from django.utils.translation import gettext_lazy as _
from django.views.decorators.http import require_GET, require_http_methods
from django.views.generic.list import ListView
from main.forms import ContactForm
from main.models import Company, SiteInfo, SiteText
from news.models import Post
from store.models import Category, Product, ProductImage


@require_GET
def index(request: HttpRequest):
    posts = Post.objects.all()[:5]
    companies = Company.objects.all()
    discountedProducts = Product.products.filter(discount__gt=0).select_related('category').prefetch_related(
                Prefetch('product_image', queryset=ProductImage.objects.filter(is_feature=True), to_attr='image_feature'),
            )
    categories = Category.objects.annotate(
        products_count=Count("product_category")).all().order_by("name")
    siteText = SiteText.objects.values('about').filter(language=get_language()).first()
    return render(request, 'main/index.html', context={"posts": posts, "companies": companies, "discounted_products": discountedProducts, "categories": categories, "about": siteText["about"]})


@require_http_methods(['GET', 'POST'])
def contact(request: HttpRequest):
    breadcrumb = [
        {"title": _("Contact Us")},
        {"title": _("Home"), "route": reverse("main:index")},
        {"title": _("Contact Us")},
    ]
    if request.method == 'POST':
        form = ContactForm(request.POST)
        siteInfo = SiteInfo.objects.first()
        if form.is_valid():
            data = form.cleaned_data
            try:
                send_mail(data["subject"], data["message"], data["email"], [os.environ.get("COMPANY_EMAIL", "")])
            except BadHeaderError:
                messages.error(request, "Email cannot be sent")
                return render(request, "main/contact.html", {"form": form, 'siteInfo': siteInfo, "breadcrumb": breadcrumb})
            messages.success(request, 'Email was sent successfully!')
            return redirect(reverse("main:contact")+"#contact-form")
        messages.error(request, "Email cannot be sent")
        return render(request, "main/contact.html", {"form": form, 'siteInfo': siteInfo, "breadcrumb": breadcrumb})
    siteInfo = SiteInfo.objects.first()
    form = ContactForm()
    return render(request, 'main/contact.html', {'siteInfo': siteInfo, "form": form, "breadcrumb": breadcrumb})


@require_GET
def about(request: HttpRequest):
    siteText = SiteText.objects.values('about').filter(language=get_language()).first()
    breadcrumb = [
        {"title": _("About Us")},
        {"title": _("Home"), "route": reverse("main:index")},
        {"title": _("About Us")},
    ]
    return render(request, 'main/about.html', {'siteText': siteText, "breadcrumb": breadcrumb})


class CareerListView(ListView):
    model = Company
    template_name = "main/career.html"
    context_object_name = "companies"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["breadcrumb"] = [
            {"title": _("Career")},
            {"title": _("Home"), "route": reverse("main:index")},
            {"title": _("Career")},
        ]
        return context
    
