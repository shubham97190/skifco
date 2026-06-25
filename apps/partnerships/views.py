from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView

from .forms import CSRInquiryForm
from .models import CSRCategory, Partner


class CSRPartnershipsView(TemplateView):
    template_name = 'partnerships/page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['partners'] = Partner.objects.filter(is_active=True)
        context['csr_categories'] = CSRCategory.objects.all()
        context['form'] = CSRInquiryForm()
        return context


class CSRInquiryCreateView(CreateView):
    form_class = CSRInquiryForm
    template_name = 'partnerships/page.html'
    success_url = reverse_lazy('partnerships:page')

    def form_valid(self, form):
        messages.success(self.request, 'Thank you for your interest! We will get back to you soon.')
        return super().form_valid(form)
