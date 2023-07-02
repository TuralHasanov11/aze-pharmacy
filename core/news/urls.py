from django.urls import path
from news import views

app_name = "news"

urlpatterns = [
    path('', views.PostListView.as_view(), name='index'),
    path('<str:slug>', views.PostDetailView.as_view(), name='detail'),
]
