from django.views.generic import DetailView, ListView

from .models import Program, ProgramCategory


class ProgramListView(ListView):
    model = Program
    template_name = 'programs/list.html'
    context_object_name = 'programs'
    paginate_by = 12

    def get_queryset(self):
        qs = super().get_queryset().filter(is_active=True).select_related('category')
        category_slug = self.request.GET.get('category')
        if category_slug:
            qs = qs.filter(category__slug=category_slug)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = ProgramCategory.objects.all()
        context['current_category'] = self.request.GET.get('category', '')
        return context


class ProgramDetailView(DetailView):
    model = Program
    template_name = 'programs/detail.html'
    context_object_name = 'program'

    def get_queryset(self):
        return super().get_queryset().filter(is_active=True).select_related('category')
