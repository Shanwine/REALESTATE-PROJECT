from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages


def admin_required(view_func):
    """Decorator to restrict views to admin users only."""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        if not request.user.is_admin_user:
            messages.error(request, 'You do not have permission to access the admin dashboard.')
            return redirect('home')
        return view_func(request, *args, **kwargs)
    return wrapper


def customer_required(view_func):
    """Decorator to restrict views to customer users only."""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        if not request.user.is_customer and not request.user.is_superuser:
            messages.error(request, 'This area is for customers only.')
            return redirect('home')
        return view_func(request, *args, **kwargs)
    return wrapper
