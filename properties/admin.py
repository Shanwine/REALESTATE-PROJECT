
from django.contrib import admin
from .models import Property, PropertyImage


class PropertyImageInline(admin.TabularInline):
    model = PropertyImage
    extra = 1


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'location', 'property_type', 'status', 'created_at')
    list_filter = ('property_type', 'status', 'is_featured')
    search_fields = ('title', 'location', 'description')
    inlines = [PropertyImageInline]


@admin.register(PropertyImage)
class PropertyImageAdmin(admin.ModelAdmin):
    list_display = ('property', 'is_primary', 'uploaded_at')