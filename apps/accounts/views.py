from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView

from apps.beneficiaries.models import Application
from apps.donations.models import Donation

from .forms import RegisterForm


class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('core:home')

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        return response


class DonorHistoryView(LoginRequiredMixin, ListView):
    template_name = 'accounts/donor_history.html'
    context_object_name = 'donations'
    paginate_by = 20

    def get_queryset(self):
        return Donation.objects.filter(donor=self.request.user, status=Donation.Status.PAID)


class MyApplicationsView(LoginRequiredMixin, ListView):
    template_name = 'accounts/my_applications.html'
    context_object_name = 'applications'

    def get_queryset(self):
        return Application.objects.filter(applicant=self.request.user).select_related('aid_type')


class ApplicationStatusView(LoginRequiredMixin, DetailView):
    template_name = 'accounts/application_status.html'
    context_object_name = 'application'

    def get_queryset(self):
        return Application.objects.filter(applicant=self.request.user).select_related('aid_type')

    def get_object(self):
        return self.get_queryset().get(reference_no=self.kwargs['ref'])
