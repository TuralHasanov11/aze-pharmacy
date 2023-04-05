from django.http import HttpRequest
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.views.generic.list import ListView
from main.models import Company
from news.models import Post


@require_http_methods(["GET"])
def index(request: HttpRequest):
    posts = Post.objects.all()[:5]
    companies = Company.objects.all()
    return render(request, 'main/index.html', context={"posts": posts, "companies": companies})


def contact(request: HttpRequest):
    return render(request, 'main/contact.html')


def about(request: HttpRequest):
    return render(request, 'main/about.html')


class CareerListView(ListView):
    model = Company
    template_name = "main/career.html"
    context_object_name = "companies"
