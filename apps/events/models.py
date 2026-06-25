from django.db import models
from django.urls import reverse

from apps.core.models import PageBase


class Event(PageBase):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    venue = models.CharField(max_length=300, blank=True)
    address = models.TextField(blank=True)
    cover_image = models.ImageField(upload_to='events/', blank=True)
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField(blank=True, null=True)
    capacity = models.PositiveIntegerField(blank=True, null=True)
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-start_datetime']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('events:detail', args=[self.slug])

    @property
    def registered_count(self):
        return self.registrations.aggregate(total=models.Sum('attendees'))['total'] or 0

    @property
    def spots_left(self):
        if self.capacity:
            return max(0, self.capacity - self.registered_count)
        return None


class EventRegistration(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='registrations')
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    attendees = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.name} — {self.event.title}'
