from django.db import models


class Partner(models.Model):
    class PartnerType(models.TextChoices):
        CSR = 'csr', 'CSR'
        INSTITUTION = 'institution', 'Institution'
        GOVERNMENT = 'govt', 'Government'
        NGO = 'ngo', 'NGO'

    name = models.CharField(max_length=200)
    logo = models.ImageField(upload_to='partners/', blank=True)
    url = models.URLField(blank=True)
    partner_type = models.CharField(max_length=20, choices=PartnerType.choices)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.name


class CSRCategory(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']
        verbose_name = 'CSR Category'
        verbose_name_plural = 'CSR Categories'

    def __str__(self):
        return self.name


class CSRInquiry(models.Model):
    org_name = models.CharField('Organisation Name', max_length=200)
    contact_person = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    csr_category = models.ForeignKey(CSRCategory, on_delete=models.SET_NULL, null=True, blank=True)
    budget_range = models.CharField(max_length=100, blank=True)
    message = models.TextField()
    is_handled = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'CSR Inquiry'
        verbose_name_plural = 'CSR Inquiries'

    def __str__(self):
        return f'{self.org_name} — {self.contact_person}'
