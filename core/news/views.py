from django.urls import reverse
from django.utils.translation import get_language
from django.utils.translation import gettext_lazy as _
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from news.models import Post


class PostListView(ListView):
    model = Post
    template_name = "news/index.html"
    paginate_by = 10
    context_object_name = "posts"

    def get_queryset(self):
        return super().get_queryset().filter(language=get_language())
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["recent_news"] = Post.objects.all().filter(language=get_language())[:4]
        context["breadcrumb"] = [
            {"title": _("News")},
            {"title": _("Home"), "route": reverse("main:index")},
            {"title": _("News")},
        ]
        return context

class PostDetailView(DetailView):
    model = Post
    template_name = "news/detail.html"
    context_object_name = "post"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["recent_news"] = Post.objects.all()[:4]
        context["breadcrumb"] = [
            {"title": _("News")},
            {"title": _("Home"), "route": reverse("main:index")},
            {"route": reverse("news:index"), "title": _("News")},
            {"title": context["post"].title},
        ]
        return context
