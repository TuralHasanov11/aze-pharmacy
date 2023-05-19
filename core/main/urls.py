from django.urls import path
from django.utils.translation import gettext_lazy as _
from main import views

app_name = "main"

urlpatterns = [
    path('', views.index, name='index'),
    path('contact', views.contact, name='contact'),
    path('about', views.about, name='about'),
    path('career', views.CareerListView.as_view(), name='career'),
    path('terms-and-conditions', views.termsAndConditions, name='terms-and-conditions'),
    path('privacy-policy', views.privacyPolicy, name='privacy-policy'),
    path('return-policy', views.returnPolicy, name='return-policy'),
    path('faq', views.FAQListView.as_view(), name='faq'),
    path('not-found', views.notFound, name='not-found'),
]
