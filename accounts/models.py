from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """Extended user model with role-based access."""

    ROLE_CHOICES = (
        ('admin', 'Administrator'),
        ('customer', 'Customer'),
    )

    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='customer')
    phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"

    @property
    def is_admin_user(self):
        return self.role == 'admin' or self.is_superuser

    @property
    def is_customer(self):
        return self.role == 'customer'
