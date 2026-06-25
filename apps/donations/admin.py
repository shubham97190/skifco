from django.contrib import admin

from .models import Donation, Receipt


class ReceiptInline(admin.StackedInline):
    model = Receipt
    extra = 0
    readonly_fields = ('receipt_no', 'pdf_file', 'eighty_g_number', 'issued_at')


@admin.register(Donation)
class DonationAdmin(admin.ModelAdmin):
    list_display = ('donor_name', 'donor_email', 'amount', 'status', 'donation_type', 'paid_at', 'created_at')
    list_filter = ('status', 'donation_type', 'created_at')
    search_fields = ('donor_name', 'donor_email', 'razorpay_order_id', 'razorpay_payment_id')
    readonly_fields = ('razorpay_order_id', 'razorpay_payment_id', 'razorpay_signature',
                       'paid_at', 'created_at')
    list_select_related = ('program',)
    inlines = [ReceiptInline]

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
