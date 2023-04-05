from django.views.generic.list import ListView
from library.models import Document


class DocumentListView(ListView):
    model = Document
    template_name = "library/index.html"
    context_object_name = "documents"
    paginate_by = 2

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["start_index"] = self.paginate_by * (context["page_obj"].number - 1)
        return context
