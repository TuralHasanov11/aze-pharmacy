from django.urls import path
from main import views

app_name = "main"

urlpatterns = [
    path('', views.index, name='index'),
    path('contact', views.contact, name='contact'),
    path('about', views.about, name='about'),
    path('career', views.CareerView.as_view(), name='career'),
]
