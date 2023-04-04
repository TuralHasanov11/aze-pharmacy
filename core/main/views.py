from django.http import HttpRequest
from django.shortcuts import render
from django.views.generic.list import ListView

from main.models import Company


def index(request: HttpRequest):
    return render(request, 'main/index.html')


def contact(request: HttpRequest):
    return render(request, 'main/contact.html')


def about(request: HttpRequest):
    return render(request, 'main/about.html')


class CareerView(ListView):
    model = Company
    template_name = "main/career.html"
    context_object_name = "companies"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
    
    
