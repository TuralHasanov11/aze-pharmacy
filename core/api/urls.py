from api import views
from django.urls import path

app_name = "api"

urlpatterns = [
    path('orders', views.orders, name='orders'),
    path('orders/<int:id>/flag', views.orderFlag, name='orderFlag'),
]
