from django.contrib import admin

from .models import InterestArea, Volunteer


@admin.register(InterestArea)
class InterestAreaAdmin(admin.ModelAdmin):
    list_display = ('name', 'order')
    list_editable = ('order',)


@admin.register(Volunteer)
class VolunteerAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'status', 'created_at')
    list_filter = ('status',)
    search_fields = ('name', 'email', 'phone')
    filter_horizontal = ('interests',)
    readonly_fields = ('created_at',)
