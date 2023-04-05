from django.views.generic.list import ListView
from services.models import Service


class ServiceListView(ListView):
    model = Service
    template_name = "services/index.html"
    context_object_name = "services"
