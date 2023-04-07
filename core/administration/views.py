from administration.forms import (CompanyForm, DocumentForm, PostForm,
                                  ServiceForm)
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.core import paginator
from django.http import HttpRequest
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.views.decorators.http import require_http_methods
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView
from library.models import Document
from main.models import Company
from news.models import Post
from services.models import Service


@require_http_methods(["GET"])
def index(request: HttpRequest):
    creator_dashboards = [
        {"name": "Services", "route": "administration:service-list"},
        {"name": "Library", "route": "administration:document-list"},
        {"name": "News", "route": "administration:post-list"},
        {"name": "Career", "route": "administration:company-list"}
    ]
    return render(request, 'administration/index.html', context={"creator_dashboards": creator_dashboards})


class ServiceListCreateView(SuccessMessageMixin, CreateView):
    model = Service
    form_class = ServiceForm
    template_name = 'administration/services/index.html'
    success_message = "%(name)s was created successfully"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['services'] = self.model.objects.all()
        return context
    
    def get_success_url(self):
        return reverse("administration:service-list")
    

class ServiceUpdateView(SuccessMessageMixin, UpdateView):
    form_class = ServiceForm
    model = Service
    template_name = 'administration/services/detail.html'
    context_object_name = 'service'
    success_message = "%(name)s was updated successfully"

    def get_success_url(self):
        return reverse("administration:service-update", kwargs={"pk": self.object.pk})
    

class ServiceDeleteView(SuccessMessageMixin, DeleteView):
    model = Service
    success_message = "Service was deleted successfully"
    success_url = reverse_lazy('administration:service-list')


class DocumentListCreateView(SuccessMessageMixin, CreateView):
    model = Document
    form_class = DocumentForm
    template_name = 'administration/documents/index.html'
    success_message = "%(name)s was created successfully"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pagination = paginator.Paginator(self.model.objects.all().values('pk', 'name', 'updated_at'), 2)
        pageNumber = self.request.GET.get('page')
        documents = pagination.get_page(pageNumber)
        context['documents'] = documents
        return context
    
    def get_success_url(self):
        return reverse("administration:document-list")
    

class DocumentUpdateView(SuccessMessageMixin, UpdateView):
    form_class = DocumentForm
    model = Document
    template_name = 'administration/documents/detail.html'
    context_object_name = 'document'
    success_message = "%(name)s was updated successfully"

    def get_success_url(self):
        return reverse("administration:document-update", kwargs={"pk": self.object.pk})
    

class DocumentDeleteView(SuccessMessageMixin, DeleteView):
    model = Document
    success_message = "Document was deleted successfully"
    success_url = reverse_lazy('administration:document-list')


class CompanyListCreateView(SuccessMessageMixin, CreateView):
    model = Company
    form_class = CompanyForm
    template_name = 'administration/companies/index.html'
    success_message = "%(name)s was created successfully"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['companies'] = self.model.objects.all()
        return context
    
    def get_success_url(self):
        return reverse("administration:company-list")
    

class CompanyUpdateView(SuccessMessageMixin, UpdateView):
    form_class = CompanyForm
    model = Company
    template_name = 'administration/companies/detail.html'
    context_object_name = 'company'
    success_message = "%(name)s was updated successfully"

    def get_success_url(self):
        return reverse("administration:company-update", kwargs={"pk": self.object.pk})
    

class CompanyDeleteView(SuccessMessageMixin, DeleteView):
    model = Company
    success_message = "Company was deleted successfully"
    success_url = reverse_lazy('administration:company-list')


class PostListView(ListView):
    model = Post
    template_name = 'administration/posts/index.html'
    paginate_by = 20
    context_object_name = "posts"
    
    def get_queryset(self):
        return super().get_queryset()

class PostDetailView(DetailView):
    model = Post
    template_name = 'administration/posts/detail.html'
    context_object_name = "post"

class PostCreateView(SuccessMessageMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'administration/posts/create.html'
    success_message = "%(title)s was created successfully"
    success_url = reverse_lazy('administration:post-list')


class PostUpdateView(SuccessMessageMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'administration/posts/edit.html'
    context_object_name = 'post'
    success_message = "%(title)s was updated successfully"

    def get_success_url(self):
        return reverse("administration:post-update", kwargs={"pk": self.object.pk})
    

class PostDeleteView(SuccessMessageMixin, DeleteView):
    model = Post
    success_message = "Post was deleted successfully"
    success_url = reverse_lazy('administration:post-list')