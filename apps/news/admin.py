from django.contrib import admin

from .models import Category, Tag, Post


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'status', 'published_at')
    list_filter = ('status', 'category', 'published_at')
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title', 'body')
    filter_horizontal = ('tags',)
    list_select_related = ('author', 'category')
    date_hierarchy = 'published_at'
