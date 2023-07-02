from api import views
from django.urls import path

app_name = "api"

urlpatterns = [
    path('cities', views.cities, name='cities'),
    path('orders/<int:id>/flag', views.orderFlag, name='order-flag'),
    path('orders/<int:id>/refund', views.orderRefund, name='order-refund'),
    path('orders/<int:id>/update-delivery', views.updateOrderDelivery, name='order-update-delivery'),
    path('checkout-form-details', views.checkoutFormDetails, name='checkout-form-details'),
    path('wishlist/add', views.wishlistAdd, name='wishlist-add'),
    path('wishlist/remove', views.wishlistRemove, name='wishlist-remove'),
    path('cart/add', views.cartAdd, name='cart-add'),
    path('cart/update', views.cartUpdate, name='cart-update'),
    path('cart/remove', views.cartRemove, name='cart-remove'),
    path("checkout", views.checkout, name="checkout"),
    path("checkout/success", views.approvePayment, name="checkout-success"),
    path("checkout/cancel", views.cancelPayment, name="checkout-cancel"),
    path("checkout/decline", views.declinePayment, name="checkout-decline"),
]
