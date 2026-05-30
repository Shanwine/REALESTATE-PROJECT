from django.db import models
from django.conf import settings
from properties.models import Property


class Transaction(models.Model):
    """Property purchase/reservation transaction."""

    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    )

    PAYMENT_METHOD_CHOICES = (
        ('cash', 'Cash'),
        ('bank_transfer', 'Bank Transfer'),
        ('financing', 'Bank Financing'),
        ('installment', 'Installment'),
    )

    listing = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='transactions')
    customer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='purchases'
    )
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, default='cash')
    transaction_date = models.DateTimeField(auto_now=True)
    notes = models.TextField(blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-transaction_date']

    def __str__(self):
        return f"Transaction #{self.pk} - {self.listing.title} by {self.customer.username}"

    @property
    def formatted_amount(self):
        return f"\u20b1{self.amount:,.2f}"
