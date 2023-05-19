
import os

from django.contrib import messages
from django.core.mail import BadHeaderError, EmailMessage
from django.db.models import Count, Prefetch
from django.http import HttpRequest
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.translation import get_language
from django.utils.translation import gettext_lazy as _
from django.views.decorators.http import require_GET, require_http_methods
from django.views.generic.list import ListView
from news.models import Post
from store.models import Category, Product, ProductImage

from main.forms import ContactForm
from main.models import Company, Question, SiteInfo, SiteText


@require_GET
def index(request: HttpRequest):
    posts = Post.objects.all()[:5]
    companies = Company.objects.all()
    discountedProducts = Product.products.filter(discount__gt=0).select_related('category').prefetch_related(
        Prefetch('product_image', queryset=ProductImage.objects.filter(
            is_feature=True), to_attr='image_feature'),
    )
    categories = Category.objects.annotate(
        products_count=Count("product_category")).all().order_by("name")
    siteText = SiteText.objects.values('about').filter(
        language=get_language()).first()
    return render(request, 'main/index.html', context={"posts": posts, "companies": companies, "discounted_products": discountedProducts,
                                                       "categories": categories, "about": siteText["about"]})


@require_http_methods(['GET', 'POST'])
def contact(request: HttpRequest):
    breadcrumb = [
        {"title": _("Contact Us")},
        {"title": _("Home"), "route": reverse("main:index")},
        {"title": _("Contact Us")},
    ]
    siteInfo = SiteInfo.objects.first()
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            try:
                content = render_to_string("main/emails/contact.html", {
                    'message': data["message"],
                    'name': data["name"],
                    'email': data["email"],
                }, request=request)

                msg = EmailMessage(
                    subject=data["subject"],
                    body=content,
                    from_email=os.environ.get("COMPANY_EMAIL_NO_REPLY", "test@test.com"),
                    to=[os.environ.get("COMPANY_EMAIL", "")],
                )
                msg.content_subtype = "html"
                msg.send(fail_silently=True)

                messages.success(request, _('Email was sent successfully!'))
                return redirect(reverse("main:contact")+"#contact-form")
            except BadHeaderError:
                messages.error(request, _("Email cannot be sent!"))
        messages.error(request, _("Email cannot be sent!"))
    else:
        form = ContactForm()
    return render(request, "main/contact.html", {'siteInfo': siteInfo, "form": form, "breadcrumb": breadcrumb})


@require_GET
def about(request: HttpRequest):
    siteText = SiteText.objects.only('about').filter(
        language=get_language()).first()
    aboutImage = SiteInfo.objects.only('about_image').first().about_image
    breadcrumb = [
        {"title": _("About Us")},
        {"title": _("Home"), "route": reverse("main:index")},
        {"title": _("About Us")},
    ]
    return render(request, 'main/about.html', {'siteText': siteText, "breadcrumb": breadcrumb, "aboutImage": aboutImage})


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


@require_GET
def termsAndConditions(request: HttpRequest):
    siteText = SiteText.objects.only('terms_and_conditions').filter(
        language=get_language()).first()
    breadcrumb = [
        {"title": _("Terms and Conditions")},
        {"title": _("Home"), "route": reverse("main:index")},
        {"title": _("Terms and Conditions")},
    ]
    return render(request, 'main/terms-and-conditions.html', context={"terms_and_conditions": siteText.terms_and_conditions,
                                                                      "breadcrumb": breadcrumb})


@require_GET
def privacyPolicy(request: HttpRequest):
    siteText = SiteText.objects.only('privacy_policy').filter(
        language=get_language()).first()
    breadcrumb = [
        {"title": _("Privacy Policy")},
        {"title": _("Home"), "route": reverse("main:index")},
        {"title": _("Privacy Policy")},
    ]
    return render(request, 'main/privacy-policy.html', context={"privacy_policy": siteText.privacy_policy, "breadcrumb": breadcrumb})


@require_GET
def returnPolicy(request: HttpRequest):
    siteText = SiteText.objects.only('return_policy').filter(
        language=get_language()).first()
    breadcrumb = [
        {"title": _("Return Policy")},
        {"title": _("Home"), "route": reverse("main:index")},
        {"title": _("Return Policy")},
    ]
    return render(request, 'main/return-policy.html', context={"return_policy": siteText.return_policy, "breadcrumb": breadcrumb})


class FAQListView(ListView):
    model = Question
    template_name = "main/faq.html"
    context_object_name = "questions"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["breadcrumb"] = [
            {"title": _("FAQ")},
            {"title": _("Home"), "route": reverse("main:index")},
            {"title": _("FAQ")},
        ]
        return context


@require_GET
def notFound(request, exception):
    return render(request, 'main/404.html')