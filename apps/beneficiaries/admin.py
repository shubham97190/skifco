from django.contrib import admin

from .models import AidType, Application, ApplicationDocument, ApplicationStatusLog


@admin.register(AidType)
class AidTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active')
    list_filter = ('is_active',)


class ApplicationDocumentInline(admin.TabularInline):
    model = ApplicationDocument
    extra = 0
    readonly_fields = ('file', 'doc_type', 'uploaded_at')

    def has_add_permission(self, request, obj=None):
        return False


class ApplicationStatusLogInline(admin.TabularInline):
    model = ApplicationStatusLog
    extra = 0
    readonly_fields = ('from_status', 'to_status', 'changed_by', 'note', 'created_at')

    def has_add_permission(self, request, obj=None):
        return False


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('reference_no', 'applicant', 'aid_type', 'status', 'assigned_to', 'created_at')
    list_filter = ('status', 'aid_type')
    search_fields = ('reference_no', 'applicant__email', 'applicant__first_name')
    list_select_related = ('applicant', 'aid_type', 'assigned_to')
    readonly_fields = ('reference_no', 'applicant', 'aid_type', 'details',
                       'requested_amount', 'created_at', 'updated_at')
    inlines = [ApplicationDocumentInline, ApplicationStatusLogInline]
