from api import views
from django.urls import path

app_name = "api"

urlpatterns = [
    path('orders', views.orders, name='orders'),
    path('cities', views.cities, name='cities'),
    path('orders/<int:id>/flag', views.orderFlag, name='order-flag'),
    path('checkout-form-details', views.checkoutFormDetails, name='checkout-form-details'),
    path('cart/add', views.cartAdd, name='cart-add'),
    path('cart/update', views.cartUpdate, name='cart-update'),
    path('cart/remove', views.cartRemove, name='cart-remove'),
    path('checkout', views.checkout, name='checkout'),
    path('wishlist/add', views.wishlistAdd, name='wishlist-add'),
    path('wishlist/remove', views.wishlistRemove, name='wishlist-remove'),
]
