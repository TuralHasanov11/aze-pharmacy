from api import views
from django.urls import path

app_name = "api"

urlpatterns = [
    path('orders', views.orders, name='orders'),
    path('cities', views.cities, name='cities'),
    path('orders/<int:id>/flag', views.orderFlag, name='orderFlag'),
    path('order-validation-messages', views.orderValidationMessages, name='order-validation-messages'),
]
