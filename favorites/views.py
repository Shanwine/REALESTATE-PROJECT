from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .models import Favorite
from properties.models import Property


@login_required
def toggle_favorite(request, property_pk):
    """Toggle a property in the user's favorites."""
    property_obj = get_object_or_404(Property, pk=property_pk)
    favorite, created = Favorite.objects.get_or_create(
        customer=request.user,
        property=property_obj
    )

    if not created:
        favorite.delete()
        is_favorited = False
        messages.info(request, f'"{property_obj.title}" removed from favorites.')
    else:
        is_favorited = True
        messages.success(request, f'"{property_obj.title}" added to favorites!')

    # Handle AJAX requests
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'is_favorited': is_favorited})

    # Regular redirect
    next_url = request.GET.get('next', request.META.get('HTTP_REFERER', '/'))
    return redirect(next_url)
