from django.views.generic import DetailView, ListView

from .models import Post


class PostListView(ListView):
    model = Post
    template_name = 'news/list.html'
    context_object_name = 'posts'
    paginate_by = 9

    def get_queryset(self):
        return super().get_queryset().filter(status=Post.Status.PUBLISHED).select_related('author', 'category')


class PostDetailView(DetailView):
    model = Post
    template_name = 'news/detail.html'
    context_object_name = 'post'

    def get_queryset(self):
        return super().get_queryset().filter(status=Post.Status.PUBLISHED).select_related('author', 'category')
