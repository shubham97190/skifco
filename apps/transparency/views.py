from django.views.generic import ListView

from .models import Report


class ReportListView(ListView):
    model = Report
    template_name = 'transparency/list.html'
    context_object_name = 'reports'

    def get_queryset(self):
        return super().get_queryset().filter(is_public=True)
