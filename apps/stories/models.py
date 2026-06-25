from django.db import models


class ImpactStory(models.Model):
    name = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='stories/', blank=True)
    quote = models.TextField()
    program = models.ForeignKey('programs.Program', on_delete=models.SET_NULL, null=True, blank=True)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Impact Stories'

    def __str__(self):
        return self.name
