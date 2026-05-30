from django.db import models
from django.conf import settings
from properties.models import Property


class Favorite(models.Model):
    """Customer's favorite/wishlist properties."""

    customer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='favorite_properties'
    )
    property = models.ForeignKey(
        Property,
        on_delete=models.CASCADE,
        related_name='favorited_by'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('customer', 'property')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.customer.username} → {self.property.title}"
