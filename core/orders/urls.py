from django.urls import path
from orders import views

app_name = "orders"

urlpatterns = [
    # path("", views.index, name="index"),
    path("<int:id>", views.detail, name="detail"),
]
