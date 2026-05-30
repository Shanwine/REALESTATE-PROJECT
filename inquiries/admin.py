from django.contrib import admin
from .models import Inquiry


@admin.register(Inquiry)
class InquiryAdmin(admin.ModelAdmin):
    list_display = ('subject', 'customer', 'property', 'status', 'created_at')
    list_filter = ('status',)
    search_fields = ('subject', 'message', 'customer__username')
