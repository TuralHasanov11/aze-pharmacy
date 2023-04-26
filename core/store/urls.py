from django.urls import path
from django.utils.translation import gettext_lazy as _
from store import views

app_name = "store"

urlpatterns = [
    path(_('products'), views.products, name='products'),
    path(_('categories')+'/<str:category_slug>/'+_('products'), views.categoryProducts, name='category-products'),
    path(_('categories')+'/<str:category_slug>/'+_('products')+'/<str:product_slug>', views.productDetail, name='product-detail'),
]
