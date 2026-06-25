from django.contrib import admin

from .models import Event, EventRegistration


class EventRegistrationInline(admin.TabularInline):
    model = EventRegistration
    extra = 0
    readonly_fields = ('name', 'email', 'phone', 'attendees', 'created_at')

    def has_add_permission(self, request, obj=None):
        return False


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'start_datetime', 'venue', 'capacity', 'is_published')
    list_filter = ('is_published', 'start_datetime')
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title', 'description', 'venue')
    inlines = [EventRegistrationInline]
