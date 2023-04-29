
from administration import forms
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import (LoginRequiredMixin,
                                        PermissionRequiredMixin)
from django.contrib.messages.views import SuccessMessageMixin
from django.core import paginator
from django.db.models import Prefetch
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
from main.models import Company, SiteInfo, SiteText
from news.models import Post
from services.models import Service
from store.models import Category, Product, ProductImage, Stock

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
    {"name": _("Orders"), "route": "administration:orders",
        "permission": "orders.view_order", "image": "images/admin/dashboards/orders.png"},
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
    success_message = "%(name)s " + _("was created successfully")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['services'] = self.model.objects.all()
        return context

    def get_success_url(self):
        return reverse("administration:service-list")


class ServiceUpdateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    form_class = forms.ServiceForm
    model = Service
    permission_required = ["services.change_service"]
    login_url = reverse_lazy('administration:index')
    template_name = 'administration/services/edit.html'
    context_object_name = 'service'
    success_message = "%(name)s " + _("was updated successfully")

    def get_success_url(self):
        return reverse("administration:service-update", kwargs={"pk": self.object.pk})


class ServiceDeleteView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Service
    permission_required = ["services.delete_service"]
    login_url = reverse_lazy('administration:index')
    success_message = _("Service") + " " + _("was deleted successfully")
    success_url = reverse_lazy('administration:service-list')


class DocumentListCreateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    model = Document
    form_class = forms.DocumentForm
    permission_required = ["library.view_document", "library.add_document"]
    login_url = reverse_lazy('administration:index')
    template_name = 'administration/documents/index.html'
    success_message = "%(name)s " + _("was created successfully")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pagination = paginator.Paginator(
            self.model.objects.all().values('pk', 'name', 'updated_at'), 2)
        pageNumber = self.request.GET.get('page')
        documents = pagination.get_page(pageNumber)
        context['documents'] = documents
        return context

    def get_success_url(self):
        return reverse("administration:document-list")


class DocumentUpdateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    form_class = forms.DocumentForm
    model = Document
    permission_required = ["library.change_document"]
    login_url = reverse_lazy('administration:index')
    template_name = 'administration/documents/edit.html'
    context_object_name = 'document'
    success_message = "%(name)s " + _("was updated successfully")

    def get_success_url(self):
        return reverse("administration:document-update", kwargs={"pk": self.object.pk})


class DocumentDeleteView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Document
    permission_required = ["library.delete_document"]
    login_url = reverse_lazy('administration:index')
    success_message = _("Document") + " " + _("was deleted successfully")
    success_url = reverse_lazy('administration:document-list')


class CompanyListCreateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    model = Company
    form_class = forms.CompanyForm
    login_url = reverse_lazy('administration:index')
    permission_required = ["main.view_company", "main.add_company"]
    template_name = 'administration/companies/index.html'
    success_message = "%(name)s " + _("was created successfully")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['companies'] = self.model.objects.all()
        return context

    def get_success_url(self):
        return reverse("administration:company-list")


class CompanyUpdateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    form_class = forms.CompanyForm
    model = Company
    permission_required = ["library.change_company"]
    login_url = reverse_lazy('administration:index')
    template_name = 'administration/companies/edit.html'
    context_object_name = 'company'
    success_message = "%(name)s " + _("was updated successfully")

    def get_success_url(self):
        return reverse("administration:company-update", kwargs={"pk": self.object.pk})


class CompanyDeleteView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Company
    permission_required = ["library.delete_document"]
    login_url = reverse_lazy('administration:index')
    success_message = _("Company") + " " + _("was deleted successfully")
    success_url = reverse_lazy('administration:company-list')


class PostListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Post
    permission_required = ["news.view_post"]
    login_url = reverse_lazy('administration:index')
    template_name = 'administration/posts/index.html'
    paginate_by = 20
    context_object_name = "posts"

    def get_queryset(self):
        return super().get_queryset()


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
    success_message = "%(title)s " + _("was created successfully")
    success_url = reverse_lazy('administration:post-list')


class PostUpdateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Post
    form_class = forms.PostForm
    permission_required = ["news.change_post"]
    login_url = reverse_lazy('administration:index')
    template_name = 'administration/posts/edit.html'
    context_object_name = 'post'
    success_message = "%(title)s " + _("was updated successfully")

    def get_success_url(self):
        return reverse("administration:post-update", kwargs={"pk": self.object.pk})


class PostDeleteView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Post
    permission_required = ["news.delete_post"]
    login_url = reverse_lazy('administration:index')
    success_message = _("Post") + " " + _("was deleted successfully")
    success_url = reverse_lazy('administration:post-list')


@require_http_methods(['GET', 'POST'])
@login_required
def profile(request):
    if request.method == 'POST':
        form = forms.UserUpdateForm(instance=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account updated successfully")
            return redirect('administration:auth-profile')
        messages.error(request, "Account could not be updated")
        return render(request, 'administration/auth/profile.html', context={
            "form": form,
        })
    form = forms.UserUpdateForm(instance=request.user)
    return render(request, 'administration/auth/profile.html', context={
        "form": form,
    })


class LoginView(auth_views.LoginView):
    authentication_form = forms.UserLoginForm
    template_name = 'administration/auth/login.html'


class LogoutView(LoginRequiredMixin, PermissionRequiredMixin, auth_views.LogoutView):
    next_page = reverse_lazy('main:index')


class PasswordChangeView(LoginRequiredMixin, auth_views.PasswordChangeView):
    template_name = 'administration/auth/password-change.html'
    success_url = reverse_lazy("administration:auth-profile")
    form_class = forms.PasswordChangeForm


class UserListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = get_user_model()
    permission_required = ["user.view_user"]
    login_url = reverse_lazy('administration:index')
    template_name = 'administration/users/index.html'
    paginate_by = 20
    context_object_name = "users"


class UserCreateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    model = get_user_model()
    form_class = forms.UserCreateForm
    permission_required = ["user.add_user"]
    login_url = reverse_lazy('administration:index')
    template_name = 'administration/users/create.html'
    success_message = "%(username)s " + _("was created successfully")
    success_url = reverse_lazy('administration:user-list')


class UserUpdateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    model = get_user_model()
    form_class = forms.UserUpdateForm
    permission_required = ["user.change_user"]
    login_url = reverse_lazy('administration:index')
    template_name = 'administration/users/edit.html'
    context_object_name = 'user'
    success_message = "%(username)s " + _("was updated successfully")

    def get_success_url(self):
        return reverse("administration:user-update", kwargs={"pk": self.object.pk})


class UserDeleteView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, DeleteView):
    model = get_user_model()
    permission_required = ["user.delete_user"]
    login_url = reverse_lazy('administration:index')
    success_message = _("User") + " " + _("was deleted successfully")
    success_url = reverse_lazy('administration:user-list')


class CategoryListCreateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    model = Category
    form_class = forms.CategoryForm
    permission_required = ["store.view_category", "store.add_category"]
    login_url = reverse_lazy('administration:index')
    template_name = 'administration/store/categories/index.html'
    success_message = "%(name)s " + _("was created successfully")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = self.model.objects.all()
        return context

    def get_success_url(self):
        return reverse("administration:store-category-list")


class CategoryUpdateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    form_class = forms.CategoryForm
    model = Category
    permission_required = ["store.change_category"]
    login_url = reverse_lazy('administration:index')
    template_name = 'administration/store/categories/edit.html'
    context_object_name = 'category'
    success_message = "%(name)s " + _("was updated successfully")

    def get_success_url(self):
        return reverse("administration:store-category-update", kwargs={"pk": self.object.pk})


class CategoryDeleteView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Category
    permission_required = ["store.delete_category"]
    login_url = reverse_lazy('administration:index')
    success_message = _("Category") + " " + _("was deleted successfully")
    success_url = reverse_lazy('administration:store-category-list')


class ProductListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Product
    permission_required = ["store.view_product"]
    login_url = reverse_lazy('administration:index')
    template_name = 'administration/store/products/index.html'
    paginate_by = 20
    context_object_name = "products"

    def get_queryset(self):
        return super().get_queryset().select_related('category').prefetch_related(
            Prefetch('product_image', queryset=ProductImage.objects.filter(is_feature=True), to_attr='image_feature'))


class ProductDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Product
    permission_required = ["store.view_product"]
    login_url = reverse_lazy('administration:index')
    template_name = 'administration/store/products/detail.html'
    context_object_name = "product"

    def get_queryset(self):
        return super().get_queryset().select_related('category', 'product_stock').prefetch_related(
            Prefetch('product_image', queryset=ProductImage.objects.filter(
                is_feature=True), to_attr='image_feature'),
            Prefetch('product_image', to_attr='images')
        )


@require_http_methods(['GET', 'POST'])
@login_required
@permission_required('store.add_product', login_url=reverse_lazy('administration:index'))
def productCreate(request):
    if request.method == 'POST':
        form = forms.ProductForm(request.POST, request.FILES)
        stock_formset = forms.StockFormSet(
            data=request.POST, files=request.FILES)
        product_image_formset = forms.ProductImageFormSet(
            data=request.POST, files=request.FILES)
        if form.is_valid() and stock_formset.is_valid() and product_image_formset.is_valid():
            product = form.save()
            for item in stock_formset:
                stock = item.save(commit=False)
                stock.product = product
                stock.save()
            for item in product_image_formset:
                productImage = item.save(commit=False)
                productImage.product = product
                productImage.save()
            messages.success(
                request, f'{product} ' + _("was saved successfully"))
            return redirect("administration:store-product-list")
        messages.error(request, _("Product") + " " + _("cannot be saved"))
        return render(request, "administration/store/products/create.html", {
            "form": form,
            "stock_formset": stock_formset,
            "product_image_formset": product_image_formset
        })
    form = forms.ProductForm()
    stock_formset = forms.StockFormSet(queryset=Stock.objects.none())
    product_image_formset = forms.ProductImageFormSet(
        queryset=ProductImage.objects.none())
    return render(request, 'administration/store/products/create.html', context={
        'form': form,
        'stock_formset': stock_formset,
        'product_image_formset': product_image_formset,
    })


@require_http_methods(['GET', 'POST'])
@login_required
@permission_required('store.change_product', login_url=reverse_lazy('administration:index'))
def productUpdate(request, pk: int):
    product = Product.objects.prefetch_related('product_image').get(id=pk)

    if request.method == 'POST':
        form = forms.ProductForm(
            instance=product, data=request.POST, files=request.FILES)
        stock_formset = forms.StockFormSet(
            instance=product, data=request.POST, files=request.FILES)
        product_image_formset = forms.ProductImageFormSet(
            instance=product, data=request.POST, files=request.FILES)
        if form.is_valid() and stock_formset.is_valid() and product_image_formset.is_valid():
            product = form.save()
            stock_formset.save()
            product_image_formset.save()
            messages.success(
                request, f'{product} ' + _("was saved successfully"))
            return redirect("administration:store-product-list")
        messages.error(request, _("Product") + " " + _("cannot be saved"))
        return render(request, "administration/store/products/edit.html", {
            "form": form,
            "stock_formset": stock_formset,
            "product_image_formset": product_image_formset,
            "product": product
        })
    form = forms.ProductForm(instance=product)
    stock_formset = forms.StockFormSet(instance=product)
    product_image_formset = forms.ProductImageFormSet(instance=product)
    return render(request, 'administration/store/products/edit.html', context={
        "product": product,
        'form': form,
        'stock_formset': stock_formset,
        'product_image_formset': product_image_formset,
    })


class ProductDeleteView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Product
    permission_required = ["store.delete_product"]
    login_url = reverse_lazy('administration:index')
    success_message = _("Product") + " " + _("was deleted successfully")
    success_url = reverse_lazy('administration:store-product-list')


class OrdersView(LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
    permission_required = ['orders.view_order', 'orders.change_order']
    login_url = reverse_lazy('administration:index')
    template_name = 'administration/orders/index.html'


@login_required
@require_http_methods(['GET', 'POST'])
@permission_required(['main.change_site_text', 'main.view_site_text',], login_url=reverse_lazy('administration:index'))
def siteTexts(request):
    if request.method == 'POST':
        formset = forms.SiteTextFormSet(initial=SiteText.objects.all(), data=request.POST)
        if formset.is_valid():
            formset.save()
            messages.success(request, _('Texts') + " " + _("were saved successfully"))
            return redirect("administration:site-texts")
        messages.error(request, _('Texts') + " " + _("cannot be saved"))
        return render('administration/site-texts.html', {"formset": formset})
    formset = forms.SiteTextFormSet(initial=SiteText.objects.all())
    return render(request, 'administration/site-texts.html', {"formset": formset})


@login_required
@require_http_methods(['GET', 'POST'])
@permission_required(['main.change_site_info', 'main.view_site_info',], login_url=reverse_lazy('administration:index'))
def siteInfo(request):
    if request.method == 'POST':
        form = forms.SiteInfoForm(instance=SiteInfo.objects.first(), data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, _('Info') + " " + _("was saved successfully"))
            return redirect("administration:site-info")
        messages.error(request, _('Info') + " " + _("cannot be saved"))
        return render('administration/site-info.html', {"form": form})
    form = forms.SiteInfoForm(instance=SiteInfo.objects.first())
    return render(request, 'administration/site-info.html', {"form": form})
