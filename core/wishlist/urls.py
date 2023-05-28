from django.urls import path
from wishlist import views

app_name = 'wishlist'

urlpatterns = [
    path('', views.index, name='index'),
]