from django.db import models


class Report(models.Model):
    class ReportType(models.TextChoices):
        ANNUAL = 'annual', 'Annual Report'
        AUDIT = 'audit', 'Audited Statement'
        IMPACT = 'impact', 'Impact Report'

    title = models.CharField(max_length=200)
    report_type = models.CharField(max_length=20, choices=ReportType.choices)
    pdf_file = models.FileField(upload_to='reports/')
    year = models.PositiveIntegerField()
    published_at = models.DateField()
    is_public = models.BooleanField(default=True)

    class Meta:
        ordering = ['-year', '-published_at']

    def __str__(self):
        return f'{self.title} ({self.year})'
