from django.contrib import admin
from .models import Transaction


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('id', 'listing', 'customer', 'amount', 'status', 'payment_method', 'transaction_date')
    list_filter = ('status', 'payment_method')
    search_fields = ('listing__title', 'customer__username')
