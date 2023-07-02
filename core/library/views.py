from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.generic.list import ListView
from library.models import Document


class DocumentListView(ListView):
    model = Document
    template_name = "library/index.html"
    context_object_name = "documents"
    paginate_by = 20

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["start_index"] = self.paginate_by * (context["page_obj"].number - 1)
        context["breadcrumb"] = [
            {"title": _("Library")},
            {"title": _("Home"), "route": reverse("main:index")},
            {"title": _("Library")},
        ]
        return context
