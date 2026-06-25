from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.generic import DetailView, FormView, TemplateView

from apps.events.models import Event
from apps.news.models import Post
from apps.partnerships.models import Partner
from apps.programs.models import Program, ProgramCategory
from apps.stories.models import ImpactStory

from .forms import ContactForm
from .models import ImpactStat, Newsletter, Page


class HomeView(TemplateView):
    template_name = 'pages/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = ProgramCategory.objects.all()
        context['featured_programs'] = Program.objects.filter(is_featured=True, is_active=True)[:6]
        context['impact_stats'] = ImpactStat.objects.all()
        context['stories'] = ImpactStory.objects.filter(is_featured=True)[:3]
        context['upcoming_events'] = Event.objects.filter(is_published=True)[:3]
        context['latest_posts'] = Post.objects.filter(status=Post.Status.PUBLISHED)[:3]
        context['partners'] = Partner.objects.filter(is_active=True)[:8]
        return context


class PageDetailView(DetailView):
    model = Page
    template_name = 'pages/page_detail.html'
    context_object_name = 'page'

    def get_queryset(self):
        return super().get_queryset().filter(is_published=True)


class ContactView(FormView):
    template_name = 'pages/contact.html'
    form_class = ContactForm
    success_url = '/contact/'

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Your message has been sent successfully. We will get back to you soon.')
        return super().form_valid(form)


@require_POST
def newsletter_subscribe(request):
    email = request.POST.get('email', '').strip()
    if not email:
        return JsonResponse({'success': False, 'message': 'Please provide an email address.'})

    _, created = Newsletter.objects.get_or_create(email=email)
    if created:
        return JsonResponse({'success': True, 'message': 'Thank you for subscribing!'})
    return JsonResponse({'success': True, 'message': 'You are already subscribed.'})
