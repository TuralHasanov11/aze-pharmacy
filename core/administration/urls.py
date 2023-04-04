from administration import views
from django.urls import path

app_name = "administration"

urlpatterns = [
    path('', views.index, name='index'),
]
