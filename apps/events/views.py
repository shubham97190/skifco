from django.contrib import messages
from django.urls import reverse
from django.views.generic import CreateView, DetailView, ListView

from .forms import EventRegistrationForm
from .models import Event


class EventListView(ListView):
    model = Event
    template_name = 'events/list.html'
    context_object_name = 'events'
    paginate_by = 9

    def get_queryset(self):
        return super().get_queryset().filter(is_published=True)


class EventDetailView(DetailView):
    model = Event
    template_name = 'events/detail.html'
    context_object_name = 'event'

    def get_queryset(self):
        return super().get_queryset().filter(is_published=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = EventRegistrationForm()
        return context


class EventRegisterView(CreateView):
    form_class = EventRegistrationForm
    template_name = 'events/detail.html'

    def form_valid(self, form):
        event = Event.objects.get(slug=self.kwargs['slug'])
        form.instance.event = event
        messages.success(self.request, 'You have been registered successfully!')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('events:detail', args=[self.kwargs['slug']])
