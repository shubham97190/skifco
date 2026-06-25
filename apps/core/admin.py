from django.contrib import admin
from solo.admin import SingletonModelAdmin

from .models import SiteConfig, ImpactStat, Page, ContactMessage, Newsletter


@admin.register(SiteConfig)
class SiteConfigAdmin(SingletonModelAdmin):
    fieldsets = (
        ('Branding', {'fields': ('name', 'tagline', 'logo', 'favicon')}),
        ('Contact', {'fields': ('contact_email', 'contact_phone', 'whatsapp_number', 'address')}),
        ('Social Media', {'fields': ('facebook_url', 'twitter_url', 'instagram_url', 'youtube_url', 'linkedin_url')}),
        ('Legal & Registration', {'fields': ('eighty_g_number', 'twelve_a_number', 'registered_address')}),
        ('Features', {'fields': ('donations_enabled',)}),
    )


@admin.register(ImpactStat)
class ImpactStatAdmin(admin.ModelAdmin):
    list_display = ('label', 'value', 'suffix', 'order')
    list_editable = ('order',)


@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'is_published', 'updated_at')
    list_filter = ('is_published',)
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title', 'body')


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'is_read', 'created_at')
    list_filter = ('is_read',)
    search_fields = ('name', 'email', 'subject')
    readonly_fields = ('name', 'email', 'phone', 'subject', 'message', 'created_at')

    def has_add_permission(self, request):
        return False


@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ('email', 'subscribed_at')
    search_fields = ('email',)

    def has_add_permission(self, request):
        return False
