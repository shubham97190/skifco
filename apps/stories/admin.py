from django.contrib import admin

from .models import ImpactStory


@admin.register(ImpactStory)
class ImpactStoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'program', 'is_featured', 'created_at')
    list_filter = ('is_featured', 'program')
    search_fields = ('name', 'quote')
