from api import views
from django.urls import path
from rest_framework.routers import DefaultRouter

app_name = "api"

router = DefaultRouter()
# router.register(r'orders', views.orders, basename="orders")

urlpatterns = [
    path('orders', views.orders, name='order-list'),
    # path('orders/<int:orderId>', views.orderDetail, name='order-detail'),
    path('orders/<int:orderId>/verify', views.verifyOrder, name='order-verify'),
]
