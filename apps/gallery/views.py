from django.views.generic import DetailView, ListView

from .models import Album


class AlbumListView(ListView):
    model = Album
    template_name = 'gallery/list.html'
    context_object_name = 'albums'
    paginate_by = 12

    def get_queryset(self):
        return super().get_queryset().filter(is_published=True)


class AlbumDetailView(DetailView):
    model = Album
    template_name = 'gallery/detail.html'
    context_object_name = 'album'

    def get_queryset(self):
        return super().get_queryset().filter(is_published=True).prefetch_related('items')
