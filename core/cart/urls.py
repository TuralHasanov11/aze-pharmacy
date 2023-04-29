from cart import views
from django.urls import path

app_name = 'cart'

urlpatterns = [
    path('', views.summary, name='index'),
    path('cart', views.cart, name='cart'),
    path('add/', views.cartAdd, name='add'),
    path('update/', views.cartUpdate, name='update'),
    path('remove/', views.cartRemove, name='remove'),
    path('wishlist/', views.wishlist, name='wishlist'),
    path('wishlist/add', views.wishlistAdd, name='wishlist-add'),
    path('wishlist/remove', views.wishlistRemove, name='wishlist-remove'),
]