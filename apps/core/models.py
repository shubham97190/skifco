from django.db import models
from solo.models import SingletonModel


class PageBase(models.Model):
    meta_title = models.CharField(max_length=70, blank=True)
    meta_description = models.CharField(max_length=160, blank=True)

    class Meta:
        abstract = True


class SiteConfig(SingletonModel):
    name = models.CharField(max_length=200, default='SKIFCO Foundation')
    tagline = models.CharField(max_length=300, blank=True)
    logo = models.ImageField(upload_to='site/', blank=True)
    favicon = models.ImageField(upload_to='site/', blank=True)

    contact_email = models.EmailField(blank=True)
    contact_phone = models.CharField(max_length=20, blank=True)
    whatsapp_number = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)

    facebook_url = models.URLField(blank=True)
    twitter_url = models.URLField(blank=True)
    instagram_url = models.URLField(blank=True)
    youtube_url = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)

    eighty_g_number = models.CharField('80G Number', max_length=100, blank=True)
    twelve_a_number = models.CharField('12A Number', max_length=100, blank=True)
    registered_address = models.TextField(blank=True)

    donations_enabled = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Site Configuration'

    def __str__(self):
        return 'Site Configuration'


class ImpactStat(models.Model):
    label = models.CharField(max_length=100)
    value = models.PositiveIntegerField()
    suffix = models.CharField(max_length=20, blank=True, help_text='e.g. "+", "K", "%"')
    icon = models.CharField(max_length=50, blank=True, help_text='Bootstrap icon class')
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']
        verbose_name = 'Impact Statistic'

    def __str__(self):
        return f'{self.label}: {self.value}{self.suffix}'


class Page(PageBase):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    body = models.TextField()
    banner = models.ImageField(upload_to='pages/', blank=True)
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Static Page'

    def __str__(self):
        return self.title


class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    subject = models.CharField(max_length=200)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.name} — {self.subject}'


class Newsletter(models.Model):
    email = models.EmailField(unique=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email
