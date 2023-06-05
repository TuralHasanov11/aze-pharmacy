from checkout import views
from django.urls import path

app_name = "checkout"

urlpatterns = [
    path("", views.index, name="index"),
    path("declined", views.declined, name="declined"),
]
