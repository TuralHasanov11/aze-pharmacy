from cart import views
from django.urls import path

app_name = 'cart'

urlpatterns = [
    path('', views.summary, name='index'),
    path('add', views.add, name='add'),
    path('update', views.update, name='update'),
    path('remove', views.remove, name='remove'),
]