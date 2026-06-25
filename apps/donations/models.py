from django.conf import settings
from django.db import models


class Donation(models.Model):
    class DonationType(models.TextChoices):
        ONE_TIME = 'one_time', 'One Time'
        RECURRING = 'recurring', 'Recurring'

    class Status(models.TextChoices):
        CREATED = 'created', 'Created'
        PAID = 'paid', 'Paid'
        FAILED = 'failed', 'Failed'
        REFUNDED = 'refunded', 'Refunded'

    donor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    donor_name = models.CharField(max_length=200)
    donor_email = models.EmailField()
    donor_phone = models.CharField(max_length=20)
    donor_pan = models.CharField('PAN Number', max_length=10, blank=True)
    donor_address = models.TextField(blank=True)

    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default='INR')
    donation_type = models.CharField(max_length=20, choices=DonationType.choices, default=DonationType.ONE_TIME)
    program = models.ForeignKey('programs.Program', on_delete=models.SET_NULL, null=True, blank=True)

    razorpay_order_id = models.CharField(max_length=100, unique=True, blank=True, null=True)
    razorpay_payment_id = models.CharField(max_length=100, blank=True)
    razorpay_signature = models.CharField(max_length=300, blank=True)

    status = models.CharField(max_length=20, choices=Status.choices, default=Status.CREATED)
    paid_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status', 'created_at']),
        ]

    def __str__(self):
        return f'₹{self.amount} by {self.donor_name} ({self.status})'


class Receipt(models.Model):
    donation = models.OneToOneField(Donation, on_delete=models.PROTECT, related_name='receipt')
    receipt_no = models.CharField(max_length=50, unique=True)
    pdf_file = models.FileField(upload_to='receipts/', blank=True)
    eighty_g_number = models.CharField('80G Number', max_length=100, blank=True)
    issued_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.receipt_no
