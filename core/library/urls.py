from django.urls import path
from library import views

app_name = "library"

urlpatterns = [
    path('', views.DocumentListView.as_view(), name='index'),
]
