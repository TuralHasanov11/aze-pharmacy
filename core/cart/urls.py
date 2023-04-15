from cart import views
from django.urls import path

app_name = 'cart'

urlpatterns = [
    path('', views.summary, name='index'),
    path('add/', views.cartAdd, name='add'),
    path('update/', views.cartUpdate, name='update'),
    path('remove/', views.cartRemove, name='remove'),
]