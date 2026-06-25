import uuid

from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import ApplicationForm
from .models import Application


class ApplicationCreateView(LoginRequiredMixin, CreateView):
    model = Application
    form_class = ApplicationForm
    template_name = 'beneficiaries/apply.html'
    success_url = reverse_lazy('accounts:my-applications')

    def form_valid(self, form):
        form.instance.applicant = self.request.user
        form.instance.reference_no = f'SKF-{uuid.uuid4().hex[:8].upper()}'
        return super().form_valid(form)
