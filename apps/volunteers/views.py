from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import VolunteerForm
from .models import InterestArea


class VolunteerSignupView(CreateView):
    form_class = VolunteerForm
    template_name = 'volunteers/signup.html'
    success_url = reverse_lazy('volunteers:signup')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['interest_areas'] = InterestArea.objects.all()
        return context

    def form_valid(self, form):
        messages.success(self.request, 'Thank you for volunteering! We will contact you soon.')
        return super().form_valid(form)
