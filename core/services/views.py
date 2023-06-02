from typing import Any, Dict

from django.urls import reverse
from django.utils.translation import get_language
from django.utils.translation import gettext_lazy as _
from django.views.generic.list import ListView
from services.models import Service


class ServiceListView(ListView):
    model = Service
    template_name = "services/index.html"
    context_object_name = "services"

    def get_queryset(self):
        return super().get_queryset().filter(language=get_language())
    

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["breadcrumb"] = [
            {"title": _("Services")},
            {"title": _("Home"), "route": reverse("main:index")},
            {"title": _("Services")},
        ]
        return context
