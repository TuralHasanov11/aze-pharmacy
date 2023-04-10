from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from news.models import Post


class PostListView(ListView):
    model = Post
    template_name = "news/index.html"
    paginate_by = 2
    context_object_name = "posts"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["popular_posts"] = Post.objects.all()[:4]
        return context

class PostDetailView(DetailView):
    model = Post
    template_name = "news/detail.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["popular_posts"] = Post.objects.all()[:4]
        return context
