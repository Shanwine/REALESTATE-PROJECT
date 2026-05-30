from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Property
from .forms import PropertySearchForm


def home(request):
    """Public landing page with featured properties."""
    featured = Property.objects.filter(is_featured=True, status='available')[:6]
    latest = Property.objects.filter(status='available')[:6]
    total_properties = Property.objects.filter(status='available').count()

    context = {
        'featured_properties': featured,
        'latest_properties': latest,
        'total_properties': total_properties,
    }
    return render(request, 'home.html', context)


def property_list(request):
    """Browse all available properties with search and filter."""
    form = PropertySearchForm(request.GET)
    properties = Property.objects.filter(status='available')

    if form.is_valid():
        keyword = form.cleaned_data.get('keyword')
        location = form.cleaned_data.get('location')
        property_type = form.cleaned_data.get('property_type')
        min_price = form.cleaned_data.get('min_price')
        max_price = form.cleaned_data.get('max_price')
        bedrooms = form.cleaned_data.get('bedrooms')

        if keyword:
            properties = properties.filter(
                Q(title__icontains=keyword) | Q(description__icontains=keyword)
            )
        if location:
            properties = properties.filter(location__icontains=location)
        if property_type:
            properties = properties.filter(property_type=property_type)
        if min_price:
            properties = properties.filter(price__gte=min_price)
        if max_price:
            properties = properties.filter(price__lte=max_price)
        if bedrooms:
            properties = properties.filter(bedrooms__gte=bedrooms)

    paginator = Paginator(properties, 9)
    page = request.GET.get('page')
    properties = paginator.get_page(page)

    context = {
        'properties': properties,
        'form': form,
    }
    return render(request, 'properties/list.html', context)


def property_detail(request, pk):
    """View full property details."""
    property_obj = get_object_or_404(Property, pk=pk)
    images = property_obj.images.all()
    related = Property.objects.filter(
        property_type=property_obj.property_type,
        status='available'
    ).exclude(pk=pk)[:3]

    # Check if user has favorited this property
    is_favorited = False
    if request.user.is_authenticated:
        is_favorited = request.user.favorite_properties.filter(property=property_obj).exists()

    context = {
        'property': property_obj,
        'images': images,
        'related_properties': related,
        'is_favorited': is_favorited,
    }
    return render(request, 'properties/detail.html', context)
