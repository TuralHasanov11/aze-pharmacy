from django.urls import path
from main import views

app_name = "main"

urlpatterns = [
    path('', views.index, name='index'),
    path('contact', views.contact, name='contact'),
    path('search', views.search, name='search'),
    path('about', views.about, name='about'),
    path('career', views.CareerListView.as_view(), name='career'),
]
