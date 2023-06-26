

from enum import StrEnum
from urllib.parse import urlencode

from administration import forms
from administration.serializers import OrderLogSerializer
from api import pagination
from api.serializers import OrderSerializer
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import (LoginRequiredMixin,
                                        PermissionRequiredMixin)
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.postgres.search import (SearchQuery, SearchRank,
                                            SearchVector)
from django.core import paginator
from django.db import transaction
from django.db.models import Prefetch, Q
from django.db.models.query import QuerySet
from django.http import HttpRequest
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.decorators.http import require_GET, require_http_methods
from django.views.generic import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView
from library.models import Document
from main.models import Company, Question, SiteInfo, SiteText
from news.models import Post
from orders.models import Order, OrderDelivery, OrderItem, OrderRefund
from rest_framework.decorators import api_view
from services.models import Service
from store.models import Category, Product, ProductImage

creator_dashboard_list = [
    {"name": _("Services"), "route": "administration:service-list",
        "permission": "services.view_service", "image": "images/admin/dashboards/services.png"},
    {"name": _("Library"), "route": "administration:document-list",
        "permission": "library.view_document", "image": "images/admin/dashboards/library.png"},
    {"name": _("News"), "route": "administration:post-list",
        "permission": "news.view_post", "image": "images/admin/dashboards/news.png"},
    {"name": _("Career"), "route": "administration:company-list",
        "permission": "main.view_company", "image": "images/admin/dashboards/career.png"},
    {"name": _("Authentication"), "route": "administration:user-list",
        "permission": "user.view_user", "image": "images/admin/dashboards/authentication.png"},
    {"name": _("Store"), "route": "administration:store-product-list",
        "permission": "store.view_product", "image": "images/admin/dashboards/store.png"},
    {"name": _("Orders"), "route": "administration:order-list",
        "permission": "orders.view_order", "image": "images/admin/dashboards/orders.png"},
    {"name": _("Site Data Management"), "route": "administration:site-info",
        "permission": "main.view_siteinfo", "image": "images/admin/dashboards/site.png"},
]


@require_GET
@login_required
def index(request: HttpRequest):
    creator_dashboards = [
        item for item in creator_dashboard_list if request.user.has_perm(item["permission"])]
    return render(request, 'administration/index.html', context={"creator_dashboards": creator_dashboards})


class ServiceListCreateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    model = Service
    form_class = forms.ServiceForm
    permission_required = ["services.view_service", "services.add_service"]
    login_url = reverse_lazy('administration:index')
    template_name = 'administration/services/index.html'
    success_url = reverse_lazy("administration:service-list")
    success_message = _("Service was created successfully!")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['services'] = self.model.objects.all().only(
            'name', 'cover_image', 'language')
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'last_modified_by': self.request.user})
        return kwargs


class ServiceUpdateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    form_class = forms.ServiceForm
    model = Service
    permission_required = ["services.change_service"]
    login_url = reverse_lazy('administration:index')
    template_name = 'administration/services/edit.html'
    context_object_name = 'service'
    success_message = _("Service was updated successfully!")

    def get_success_url(self):
        return reverse("administration:service-update", kwargs={"pk": self.object.pk})

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'last_modified_by': self.request.user})
        return kwargs


class ServiceDeleteView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Service
    permission_required = ["services.delete_service"]
    login_url = reverse_lazy('administration:index')
    success_message = _("Service was deleted successfully!")
    success_url = reverse_lazy('administration:service-list')


class DocumentListCreateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    model = Document
    form_class = forms.DocumentForm
    permission_required = ["library.view_document", "library.add_document"]
    login_url = reverse_lazy('administration:index')
    success_url = reverse_lazy("administration:document-list")
    template_name = 'administration/documents/index.html'
    paginate_py = 20
    success_message = _("Document was created successfully!")

    def get_queryset(self):
        queryset = super().get_queryset().order_by(self.request.GET.get(
            'order_by', '-created_at'))
        if self.request.GET.get('search'):
            queryset = queryset.filter(
                name__icontains=self.request.GET.get('search'))
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pagination = paginator.Paginator(self.get_queryset(), self.paginate_py)
        pageNumber = self.request.GET.get('page')
        documents = pagination.get_page(pageNumber)
        context['documents'] = documents
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'last_modified_by': self.request.user})
        return kwargs


class DocumentUpdateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    form_class = forms.DocumentForm
    model = Document
    permission_required = ["library.change_document"]
    login_url = reverse_lazy('administration:index')
    template_name = 'administration/documents/edit.html'
    context_object_name = 'document'
    success_message = _("Document was updated successfully!")

    def get_success_url(self):
        return reverse("administration:document-update", kwargs={"pk": self.object.pk})

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'last_modified_by': self.request.user})
        return kwargs


class DocumentDeleteView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Document
    permission_required = ["library.delete_document"]
    login_url = reverse_lazy('administration:index')
    success_message = _("Document was deleted successfully!")
    success_url = reverse_lazy('administration:document-list')

    def get_success_url(self) -> str:
        return reverse('administration:document-list') + f"?{urlencode({'page': self.request.GET.get('page', 1)})}"


class CompanyListCreateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    model = Company
    form_class = forms.CompanyForm
    login_url = reverse_lazy('administration:index')
    permission_required = ["main.view_company", "main.add_company"]
    template_name = 'administration/companies/index.html'
    success_url = reverse_lazy("administration:company-list")
    success_message = _("Company was created successfully!")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['companies'] = self.model.objects.all()
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'last_modified_by': self.request.user})
        return kwargs


class CompanyUpdateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    form_class = forms.CompanyForm
    model = Company
    permission_required = ["library.change_company"]
    login_url = reverse_lazy('administration:index')
    template_name = 'administration/companies/edit.html'
    context_object_name = 'company'
    success_message = _("Company was updated successfully!")

    def get_success_url(self):
        return reverse("administration:company-update", kwargs={"pk": self.object.pk})

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'last_modified_by': self.request.user})
        return kwargs


class CompanyDeleteView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Company
    permission_required = ["library.delete_document"]
    login_url = reverse_lazy('administration:index')
    success_message = _("Company was deleted successfully!")
    success_url = reverse_lazy('administration:company-list')


class PostListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Post
    permission_required = ["news.view_post"]
    login_url = reverse_lazy('administration:index')
    template_name = 'administration/posts/index.html'
    paginate_by = 20
    context_object_name = "posts"

    def get_queryset(self):
        queryset = super().get_queryset().order_by(
            self.request.GET.get('order_by', '-created_at')).only('title', 'cover_image', 'language', 'created_at', 'updated_at')
        if self.request.GET.get('search'):
            queryset = queryset.filter(
                title__icontains=self.request.GET.get('search'))
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pagination = paginator.Paginator(self.get_queryset(), self.paginate_by)
        pageNumber = self.request.GET.get('page')
        posts = pagination.get_page(pageNumber)
        context['posts'] = posts
        return context


class PostDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Post
    permission_required = ["news.view_post"]
    login_url = reverse_lazy('administration:index')
    template_name = 'administration/posts/detail.html'
    context_object_name = "post"


class PostCreateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    model = Post
    form_class = forms.PostForm
    permission_required = ["news.add_post"]
    login_url = reverse_lazy('administration:index')
    template_name = 'administration/posts/create.html'
    success_message = _("Post was created successfully!")
    success_url = reverse_lazy('administration:post-list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'last_modified_by': self.request.user})
        return kwargs


class PostUpdateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Post
    form_class = forms.PostForm
    permission_required = ["news.change_post"]
    login_url = reverse_lazy('administration:index')
    template_name = 'administration/posts/edit.html'
    context_object_name = 'post'
    success_message = _("Post was updated successfully!")

    def get_success_url(self):
        return reverse("administration:post-update", kwargs={"pk": self.object.pk})

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'last_modified_by': self.request.user})
        return kwargs


class PostDeleteView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Post
    permission_required = ["news.delete_post"]
    login_url = reverse_lazy('administration:index')
    success_message = _("Post was deleted successfully!")

    def get_success_url(self) -> str:
        return reverse('administration:post-list') + f"?{urlencode({'page': self.request.GET.get('page', 1)})}"


@require_http_methods(['GET', 'POST'])
@login_required
def profile(request):
    return render(request, 'administration/auth/profile.html')


class LoginView(auth_views.LoginView):
    authentication_form = forms.UserLoginForm
    redirect_field_name = reverse_lazy("administration:index")
    redirect_authenticated_user = True
    template_name = 'administration/auth/login.html'


class LogoutView(LoginRequiredMixin, auth_views.LogoutView):
    next_page = reverse_lazy('main:index')


class PasswordChangeView(LoginRequiredMixin, auth_views.PasswordChangeView):
    template_name = 'administration/auth/password-change.html'
    success_url = reverse_lazy("administration:auth-profile")
    form_class = forms.PasswordChangeForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["example_password"] = get_user_model(
        ).objects.make_random_password(12)
        return context


class UserListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = get_user_model()
    permission_required = ["user.view_user"]
    login_url = reverse_lazy('administration:index')
    template_name = 'administration/users/index.html'
    paginate_by = 20
    context_object_name = "users"

    def get_queryset(self):
        return super().get_queryset().only('username', 'email', 'last_login_at')


class UserCreateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    model = get_user_model()
    form_class = forms.UserCreateForm
    permission_required = ["user.add_user"]
    login_url = reverse_lazy('administration:index')
    template_name = 'administration/users/create.html'
    success_message = _("User was created successfully!")
    success_url = reverse_lazy('administration:user-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["example_password"] = self.model.objects.make_random_password(
            12)
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'last_modified_by': self.request.user})
        return kwargs


class UserUpdateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    model = get_user_model()
    form_class = forms.UserUpdateForm
    permission_required = ["user.change_user"]
    login_url = reverse_lazy('administration:index')
    template_name = 'administration/users/edit.html'
    context_object_name = 'user'
    success_message = _("User was updated successfully!")

    def get_success_url(self):
        return reverse("administration:user-update", kwargs={"pk": self.object.pk})

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'last_modified_by': self.request.user})
        return kwargs


class UserDeleteView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, DeleteView):
    model = get_user_model()
    permission_required = ["user.delete_user"]
    login_url = reverse_lazy('administration:index')
    success_message = _("User was deleted successfully!")
    success_url = reverse_lazy('administration:user-list')


class UserPasswordChangeView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    model = get_user_model()
    form_class = forms.PasswordResetForm
    permission_required = ["user.change_user"]
    login_url = reverse_lazy('administration:index')
    template_name = 'administration/users/password_change.html'
    context_object_name = 'user'
    success_message = _("User's password was changed successfully!")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["example_password"] = self.model.objects.make_random_password(
            12)
        return context

    def get_success_url(self):
        return reverse("administration:user-update", kwargs={"pk": self.object.pk})

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'last_modified_by': self.request.user})
        return kwargs


class CategoryListCreateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    model = Category
    form_class = forms.CategoryForm
    permission_required = ["store.view_category", "store.add_category"]
    login_url = reverse_lazy('administration:index')
    template_name = 'administration/store/categories/index.html'
    success_message = _("Category was created successfully!")
    success_url = reverse_lazy("administration:store-category-list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = self.model.objects.add_related_count(Category.objects.all(), Product,
                                                                     'category', 'products_count',
                                                                     cumulative=True).all()
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'last_modified_by': self.request.user})
        return kwargs


class CategoryUpdateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    form_class = forms.CategoryForm
    model = Category
    permission_required = ["store.change_category"]
    login_url = reverse_lazy('administration:index')
    template_name = 'administration/store/categories/edit.html'
    context_object_name = 'category'
    success_message = _("Category was updated successfully!")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print(context["category"].has_products) 
        return context
    
    def get_success_url(self):
        return reverse("administration:store-category-update", kwargs={"pk": self.object.pk})

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'last_modified_by': self.request.user})
        return kwargs


class CategoryDeleteView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Category
    permission_required = ["store.delete_category"]
    login_url = reverse_lazy('administration:index')
    success_message = _("Category was deleted successfully!")
    success_url = reverse_lazy('administration:store-category-list')


class ProductListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Product
    permission_required = ["store.view_product"]
    login_url = reverse_lazy('administration:index')
    template_name = 'administration/store/products/index.html'
    paginate_by = 20
    context_object_name = "products"

    def get_queryset(self):
        queryset = super().get_queryset().select_related('category').prefetch_related(
            Prefetch('product_image', queryset=ProductImage.objects.filter(is_feature=True), to_attr='image_feature')).only(
                'name', 'sku', 'regular_price', 'discount', 'discount_price', 'category', 'is_active', 'updated_at').order_by(self.request.GET.get(
                    'order_by', '-created_at'))
        if self.request.GET.get('search'):
            queryset = queryset.filter(
                name__icontains=self.request.GET.get('search'))
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pagination = paginator.Paginator(self.get_queryset(), self.paginate_by)
        pageNumber = self.request.GET.get('page')
        products = pagination.get_page(pageNumber)
        context['products'] = products
        context["filter_form"] = forms.ProductFilterForm(data=self.request.GET)
        return context


class ProductDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Product
    permission_required = ["store.view_product"]
    login_url = reverse_lazy('administration:index')
    template_name = 'administration/store/products/detail.html'
    context_object_name = "product"

    def get_queryset(self):
        return super().get_queryset().select_related('category').prefetch_related(
            Prefetch('product_image', queryset=ProductImage.objects.filter(
                is_feature=True), to_attr='image_feature'),
            Prefetch('product_image', to_attr='images')
        )


@require_http_methods(['GET', 'POST'])
@login_required
@permission_required('store.add_product', login_url=reverse_lazy('administration:index'))
def productCreate(request):
    if request.method == 'POST':
        form = forms.ProductForm(
            request.POST, request.FILES, last_modified_by=request.user)
        product_image_formset = forms.ProductImageFormSet(
            data=request.POST, files=request.FILES)
        if form.is_valid() and product_image_formset.is_valid():
            with transaction.atomic():
                product = form.save()
                for item in product_image_formset:
                    productImage = item.save(commit=False)
                    productImage.product = product
                    productImage.save()
                messages.success(
                    request, _("Product was saved successfully!"))
                return redirect("administration:store-product-list")
        messages.error(request, _("Product cannot be saved!"))
    else:
        form = forms.ProductForm()
        product_image_formset = forms.ProductImageFormSet(
            queryset=ProductImage.objects.none())
    return render(request, "administration/store/products/create.html", context={
        'form': form,
        'product_image_formset': product_image_formset,
    })


@require_http_methods(['GET', 'POST'])
@login_required
@permission_required('store.change_product', login_url=reverse_lazy('administration:index'))
def productUpdate(request, pk: int):
    product = Product.objects.prefetch_related('product_image').get(id=pk)

    if request.method == 'POST':
        form = forms.ProductForm(
            instance=product, data=request.POST, files=request.FILES, last_modified_by=request.user)
        product_image_formset = forms.ProductImageFormSet(
            instance=product, data=request.POST, files=request.FILES)
        if form.is_valid() and product_image_formset.is_valid():
            with transaction.atomic():
                product = form.save()
                product_image_formset.save()
                messages.success(
                    request, _("Product was saved successfully!"))
                return redirect("administration:store-product-list")
        messages.error(request, _("Product cannot be saved!"))
    else:
        form = forms.ProductForm(instance=product)
        product_image_formset = forms.ProductImageFormSet(instance=product)

    return render(request, "administration/store/products/edit.html", context={
        "product": product,
        'form': form,
        'product_image_formset': product_image_formset,
    })


class ProductDeleteView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Product
    permission_required = ["store.delete_product"]
    login_url = reverse_lazy('administration:index')
    success_message = _("Product was deleted successfully!")

    def get_success_url(self) -> str:
        return reverse('administration:store-product-list') + f"?{urlencode({'page': self.request.GET.get('page', 1)})}"


class OrdersView(LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
    permission_required = ['orders.view_order', 'orders.change_order']
    login_url = reverse_lazy('administration:index')
    template_name = 'administration/orders/index.html'


@login_required
@require_http_methods(['GET', 'POST'])
@permission_required(['main.change_sitetext', 'main.view_sitetext'], login_url=reverse_lazy('administration:index'))
def siteTexts(request):
    if request.method == 'POST':
        formset = forms.SiteTextFormSet(
            initial=SiteText.objects.all().order_by('language'), data=request.POST)
        if formset.is_valid():
            formset.save()
            messages.success(request, _("Texts were saved successfully!"))
            return redirect("administration:site-texts")
        messages.error(request, _("Texts cannot be saved!"))
    else:
        formset = forms.SiteTextFormSet(initial=SiteText.objects.all())
    return render(request, 'administration/site/texts.html', {"formset": formset})


@login_required
@require_http_methods(['GET', 'POST'])
@permission_required(['main.change_siteinfo', 'main.view_siteinfo'], login_url=reverse_lazy('administration:index'))
def siteInfo(request):
    siteInfo = SiteInfo.objects.first()
    if request.method == 'POST':
        if siteInfo:
            form = forms.SiteInfoForm(
                instance=siteInfo, data=request.POST, files=request.FILES, last_modified_by=request.user)
        else:
            form = forms.SiteInfoForm(
                data=request.POST, files=request.FILES, last_modified_by=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, _("Site Info was saved successfully!"))
            return redirect("administration:site-info")
        messages.error(request, _("Site Info cannot be saved!"))
    else:
        form = forms.SiteInfoForm(instance=siteInfo)
    return render(request, 'administration/site/info.html', {"form": form, "site_info": siteInfo})


class FAQListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Question
    permission_required = ["main.view_question"]
    login_url = reverse_lazy('administration:index')
    template_name = 'administration/site/faq-list.html'
    context_object_name = "questions"

    def get_queryset(self):
        return super().get_queryset().only('pk', 'question', 'language')


class FAQCreateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    model = Question
    form_class = forms.FAQForm
    permission_required = ["main.add_question"]
    login_url = reverse_lazy('administration:index')
    template_name = 'administration/site/faq-create.html'
    success_message = _("Question was created successfully!")
    success_url = reverse_lazy('administration:site-faq-list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'last_modified_by': self.request.user})
        return kwargs


class FAQUpdateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Question
    form_class = forms.FAQForm
    permission_required = ["main.change_question"]
    login_url = reverse_lazy('administration:index')
    template_name = 'administration/site/faq-edit.html'
    context_object_name = 'question'
    success_message = _("Question was updated successfully!")

    def get_success_url(self):
        return reverse("administration:site-faq-update", kwargs={"pk": self.object.pk})

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'last_modified_by': self.request.user})
        return kwargs


class FAQDeleteView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Question
    permission_required = ["main.delete_question"]
    login_url = reverse_lazy('administration:index')
    success_message = _("Question was deleted successfully!")
    success_url = reverse_lazy('administration:site-faq-list')


@login_required
@require_http_methods(['GET', 'POST'])
@permission_required(["orders.change_order", "orders.view_order"], login_url=reverse_lazy('administration:index'))
def orderDetail(request, id: int):
    template_name = 'administration/orders/detail.html'
    success_message = _("Order was updated successfully!")
    order = Order.objects.select_related('order_delivery').prefetch_related(
        Prefetch('items', queryset=OrderItem.objects.select_related(
            'product__category').all()),
        Prefetch('refunds', queryset=OrderRefund.objects.all())
    ).get(id=id)

    if request.POST:
        form = forms.OrderForm(data=request.POST, instance=order)
        if form.is_valid():
            instance = form.save()
            logsSerializer = OrderLogSerializer(instance=instance,
                                                logs=instance.history.order_by('-history_date'))
            logsSerializer.save()

            messages.success(request, success_message)
            return redirect(reverse("administration:order-detail", kwargs={"id": order.id})+"#order-form")
        messages.error(request, _("Order was not saved!"))
    else:
        if not order.seen:
            order.seen = True
            order.save()
        form = forms.OrderForm(instance=order)

    orderLogs = order.history.exclude(
        history_change_reason=None).order_by('-history_date')

    context = {
        "order": order,
        "form": form,
        "order_logs": orderLogs,
    }

    if hasattr(order, "order_delivery"):
        context["delivery_form"] = forms.OrderDeliveryForm(
            instance=OrderDelivery.objects.get(order=order))
        context["order_delivery_logs"] = order.order_delivery.history.exclude(history_change_reason=None).order_by(
            '-history_date')

    if order.payment_status == Order.PaymentStatus.PAID:
        context["refund_form"] = forms.OrderRefundForm()

    return render(request, template_name, context)


class OrderPaymentStatusFilterQuery:
    class Values(StrEnum):
        PENDING: str = "PENDING"
        PAID: str = "PAID"
        FAILED: str = "FAILED"
        REFUNDED: str = "REFUNDED"

    queryset: QuerySet

    def __init__(self, queryset, status: str = None) -> None:
        self.queryset = queryset
        if status is not None and status.upper() in self.values:
            self.queryset = self.queryset.filter(payment_status=status.upper())

    @property
    def values(self):
        return [item.value for item in self.Values]


class OrderFlaggedFilterQuery:
    queryset: QuerySet

    def __init__(self, queryset, value=False) -> None:
        self.queryset = queryset
        if value is not False:
            self.queryset = self.queryset.filter(is_flagged=bool(value))


class OrderSearchFilterQuery:
    queryset: QuerySet

    def __init__(self, queryset, value: str) -> None:
        self.queryset = queryset
        if value:
            self.queryset = self.queryset.filter(Q(id__icontains=value) | Q(first_name__icontains=value) |
                                                 Q(last_name__icontains=value) | Q(email__icontains=value) |
                                                 Q(address__icontains=value) | Q(city__icontains=value) |
                                                 Q(phone__icontains=value) | Q(total_paid__icontains=value) |
                                                 Q(order_id__icontains=value) | Q(notes__icontains=value))


@login_required
@api_view(['GET'])
@permission_required(['orders.view_order', 'orders.change_order'], raise_exception=True)
def orders(request):
    ordersQueryset = OrderPaymentStatusFilterQuery(
        OrderFlaggedFilterQuery(OrderSearchFilterQuery(Order.objects.all(), request.GET.get(
            'search', None)).queryset, request.GET.get('is_flagged', False)).queryset,
        request.GET.get('status', None)).queryset.order_by(request.GET.get('order_by', '-created_at'))

    paginator = pagination.OrderPagination()
    orders = paginator.paginate_queryset(ordersQueryset, request)
    serializer = OrderSerializer(orders, many=True)
    return paginator.get_paginated_response(serializer.data)
