from django.db import models
from django.conf import settings
from django.utils import timezone

# Create your models here.

class Task(models.Model):
    STATUS_CHOICES = [
        ('todo', 'ToDo'),
        ('inprogress', 'InProgress'),
        ('done', 'Done'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='tasks')
    title = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='todo')
    total_minutes = models.DurationField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def calculate_duration(self):
        """
        Calculates and updates the total duration from created_at to now.
        """
        self.total_minutes = timezone.now() - self.created_at
        self.save(update_fields=['total_minutes'])

