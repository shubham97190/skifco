from django.contrib import admin

from .models import Partner, CSRCategory, CSRInquiry


@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
    list_display = ('name', 'partner_type', 'is_active', 'order')
    list_filter = ('partner_type', 'is_active')
    list_editable = ('order', 'is_active')


@admin.register(CSRCategory)
class CSRCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'order')
    list_editable = ('order',)


@admin.register(CSRInquiry)
class CSRInquiryAdmin(admin.ModelAdmin):
    list_display = ('org_name', 'contact_person', 'email', 'is_handled', 'created_at')
    list_filter = ('is_handled', 'csr_category')
    search_fields = ('org_name', 'contact_person', 'email')
    readonly_fields = ('org_name', 'contact_person', 'email', 'phone', 'csr_category',
                       'budget_range', 'message', 'created_at')

    def has_add_permission(self, request):
        return False
