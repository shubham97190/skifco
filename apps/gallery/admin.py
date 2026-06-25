from django.contrib import admin

from .models import Album, MediaItem


class MediaItemInline(admin.TabularInline):
    model = MediaItem
    extra = 1
    fields = ('media_type', 'file', 'video_url', 'caption', 'order')


@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_published', 'created_at')
    list_filter = ('is_published',)
    prepopulated_fields = {'slug': ('title',)}
    inlines = [MediaItemInline]
