from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomerRegistrationForm, CustomLoginForm, UserProfileForm


def register_view(request):
    """Handle customer registration."""
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful! Welcome to EstateHub.')
            return redirect('customer_dashboard')
    else:
        form = CustomerRegistrationForm()

    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    """Handle user login with role-based redirect."""
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = CustomLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Welcome back, {user.first_name or user.username}!')

            # Role-based redirect
            if user.is_admin_user:
                return redirect('admin_dashboard')
            else:
                return redirect('customer_dashboard')
    else:
        form = CustomLoginForm()

    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    """Handle user logout."""
    logout(request)
    messages.info(request, 'You have been logged out successfully.')
    return redirect('home')


@login_required
def profile_view(request):
    """Handle user profile editing."""
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
    else:
        form = UserProfileForm(instance=request.user)

    return render(request, 'accounts/profile.html', {'form': form})
