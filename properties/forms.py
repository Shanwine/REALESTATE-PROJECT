
from django import forms
from .models import Property, PropertyImage


class PropertyForm(forms.ModelForm):
    """Form for creating/editing properties."""

    class Meta:
        model = Property
        fields = [
            'title', 'description', 'price', 'location', 'address',
            'bedrooms', 'bathrooms', 'area_sqft', 'property_type',
            'status', 'is_featured',
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Property Title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Property Description'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Price'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City / Area'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Full Address'}),
            'bedrooms': forms.NumberInput(attrs={'class': 'form-control'}),
            'bathrooms': forms.NumberInput(attrs={'class': 'form-control'}),
            'area_sqft': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Area in sq ft'}),
            'property_type': forms.Select(attrs={'class': 'form-select'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'is_featured': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class PropertyImageForm(forms.ModelForm):
    """Form for uploading property images."""

    class Meta:
        model = PropertyImage
        fields = ['image', 'is_primary']
        widgets = {
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'is_primary': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class PropertySearchForm(forms.Form):
    """Search and filter form for properties."""

    keyword = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search by keyword...',
        })
    )
    location = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Location',
        })
    )
    property_type = forms.ChoiceField(
        required=False,
        choices=[('', 'All Types')] + list(Property.PROPERTY_TYPE_CHOICES),
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    min_price = forms.DecimalField(
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Min Price',
        })
    )
    max_price = forms.DecimalField(
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Max Price',
        })
    )
    bedrooms = forms.IntegerField(
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Min Bedrooms',
        })
    )