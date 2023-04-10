from cart import views
from django.urls import path

app_name = 'cart'

urlpatterns = [
    path('', views.cart, name='index'),
    path('add/', views.cartAdd, name='add'),
    path('update/', views.cartUpdate, name='update'),
    path('delete/', views.cartDelete, name='delete'),
]