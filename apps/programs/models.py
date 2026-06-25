from django.db import models
from django.urls import reverse

from apps.core.models import PageBase


class ProgramCategory(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    icon = models.CharField(max_length=50, blank=True, help_text='Bootstrap icon class')
    description = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']
        verbose_name_plural = 'Program Categories'

    def __str__(self):
        return self.name


class Program(PageBase):
    category = models.ForeignKey(ProgramCategory, on_delete=models.PROTECT, related_name='programs')
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    summary = models.TextField(help_text='Short description for cards')
    body = models.TextField()
    cover_image = models.ImageField(upload_to='programs/', blank=True)
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    start_date = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-is_featured', '-created_at']
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['category', 'is_active']),
        ]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('programs:detail', args=[self.slug])


class SDGGoal(models.Model):
    number = models.PositiveIntegerField(unique=True)
    title = models.CharField(max_length=200)
    programs = models.ManyToManyField(Program, blank=True, related_name='sdg_goals')

    class Meta:
        ordering = ['number']
        verbose_name = 'SDG Goal'

    def __str__(self):
        return f'SDG {self.number}: {self.title}'
