from django.urls import path
from services import views

app_name = "services"

urlpatterns = [
    path('', views.ServiceListView.as_view(), name='index'),
]
