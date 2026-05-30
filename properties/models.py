
from django.db import models
from django.conf import settings


class Property(models.Model):
    """Real estate property listing."""

    PROPERTY_TYPE_CHOICES = (
        ('house', 'House'),
        ('condo', 'Condominium'),
        ('townhouse', 'Townhouse'),
        ('apartment', 'Apartment'),
        ('lot', 'Lot'),
        ('commercial', 'Commercial'),
    )

    STATUS_CHOICES = (
        ('available', 'Available'),
        ('reserved', 'Reserved'),
        ('sold', 'Sold'),
    )

    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=12, decimal_places=2)
    location = models.CharField(max_length=255)
    address = models.TextField(blank=True, null=True)
    bedrooms = models.PositiveIntegerField(default=0)
    bathrooms = models.PositiveIntegerField(default=0)
    area_sqft = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    property_type = models.CharField(max_length=20, choices=PROPERTY_TYPE_CHOICES, default='house')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')
    agent = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='listed_properties'
    )
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Properties'
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    @property
    def primary_image(self):
        """Get the primary image or first image."""
        img = self.images.filter(is_primary=True).first()
        if not img:
            img = self.images.first()
        return img

    @property
    def formatted_price(self):
        """Return formatted price with commas."""
        return f"₱{self.price:,.2f}"


class PropertyImage(models.Model):
    """Images associated with a property."""

    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='properties/')
    is_primary = models.BooleanField(default=False)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image for {self.property.title}"