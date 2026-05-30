from django.db import models
from django.conf import settings
from properties.models import Property


class Inquiry(models.Model):
    """Customer inquiry/message about a property."""

    STATUS_CHOICES = (
        ('new', 'New'),
        ('read', 'Read'),
        ('replied', 'Replied'),
    )

    property = models.ForeignKey(
        Property,
        on_delete=models.CASCADE,
        related_name='inquiries',
        null=True,
        blank=True
    )
    customer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='inquiries'
    )
    subject = models.CharField(max_length=200)
    message = models.TextField()
    admin_reply = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='new')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Inquiries'
        ordering = ['-created_at']

    def __str__(self):
        return f"Inquiry: {self.subject} by {self.customer.username}"
