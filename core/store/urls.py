from django.urls import path
from store import views

app_name = "store"

urlpatterns = [
    path('products', views.products, name='products'),
    path('categories/<str:category_slug>/products', views.categoryProducts, name='category-products'),
    path('categories/<str:category_slug>/products/<str:product_slug>', views.productDetail, name='product-detail'),
]
