from django.contrib import admin

from .models import ProgramCategory, Program, SDGGoal


@admin.register(ProgramCategory)
class ProgramCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'order')
    list_editable = ('order',)
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'is_featured', 'is_active', 'updated_at')
    list_filter = ('category', 'is_featured', 'is_active')
    list_editable = ('is_featured', 'is_active')
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title', 'summary', 'body')
    list_select_related = ('category',)


@admin.register(SDGGoal)
class SDGGoalAdmin(admin.ModelAdmin):
    list_display = ('number', 'title')
    filter_horizontal = ('programs',)
