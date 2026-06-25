from django.views.generic import ListView

from .models import ImpactStory


class ImpactStoryListView(ListView):
    model = ImpactStory
    template_name = 'stories/list.html'
    context_object_name = 'stories'
