from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Sum, Count, Q
from django.db.models.functions import TruncMonth   
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.utils import timezone
from datetime import timedelta

from .decorators import admin_required, customer_required
from properties.models import Property, PropertyImage
from properties.forms import PropertyForm
from transactions.models import Transaction
from inquiries.models import Inquiry
from inquiries.forms import InquiryReplyForm
from favorites.models import Favorite
from accounts.models import CustomUser


# ─────────────────────────────────────────────
# ADMIN DASHBOARD VIEWS
# ─────────────────────────────────────────────

@admin_required
def admin_dashboard(request):
    """Admin overview with key stats."""
    total_properties = Property.objects.count()
    available_properties = Property.objects.filter(status='available').count()
    sold_properties = Property.objects.filter(status='sold').count()
    reserved_properties = Property.objects.filter(status='reserved').count()
    total_customers = CustomUser.objects.filter(role='customer').count()
    pending_inquiries = Inquiry.objects.filter(status='new').count()
    total_revenue = Transaction.objects.filter(status='completed').aggregate(
        total=Sum('amount')
    )['total'] or 0
    pending_transactions = Transaction.objects.filter(status='pending').count()

    # Recent activity
    recent_properties = Property.objects.order_by('-created_at')[:5]
    recent_transactions = Transaction.objects.order_by('-transaction_date')[:5]
    recent_inquiries = Inquiry.objects.order_by('-created_at')[:5]

    # Monthly sales data for chart (last 6 months)
    six_months_ago = timezone.now() - timedelta(days=180)
    monthly_sales = (
        Transaction.objects
        .filter(status='completed', transaction_date__gte=six_months_ago)
        .annotate(month=TruncMonth('transaction_date'))
        .values('month')
        .annotate(total=Sum('amount'), count=Count('id'))
        .order_by('month')
    )

    # Property type distribution for chart
    type_distribution = (
        Property.objects
        .values('property_type')
        .annotate(count=Count('id'))
        .order_by('-count')
    )

    context = {
        'total_properties': total_properties,
        'available_properties': available_properties,
        'sold_properties': sold_properties,
        'reserved_properties': reserved_properties,
        'total_customers': total_customers,
        'pending_inquiries': pending_inquiries,
        'total_revenue': total_revenue,
        'pending_transactions': pending_transactions,
        'recent_properties': recent_properties,
        'recent_transactions': recent_transactions,
        'recent_inquiries': recent_inquiries,
        'monthly_sales': list(monthly_sales),
        'type_distribution': list(type_distribution),
    }
    return render(request, 'dashboard/admin/index.html', context)


@admin_required
def admin_properties(request):
    """Admin property management list."""
    properties = Property.objects.all()

    # Filter by status
    status = request.GET.get('status')
    if status:
        properties = properties.filter(status=status)

    # Search
    search = request.GET.get('search')
    if search:
        properties = properties.filter(
            Q(title__icontains=search) | Q(location__icontains=search)
        )

    paginator = Paginator(properties, 10)
    page = request.GET.get('page')
    properties = paginator.get_page(page)

    context = {'properties': properties, 'current_status': status, 'search': search or ''}
    return render(request, 'dashboard/admin/properties.html', context)


@admin_required
def admin_property_add(request):
    """Add a new property."""
    if request.method == 'POST':
        form = PropertyForm(request.POST)
        images = request.FILES.getlist('images')

        if form.is_valid():
            property_obj = form.save(commit=False)
            property_obj.agent = request.user
            property_obj.save()

            for i, img in enumerate(images):
                PropertyImage.objects.create(
                    property=property_obj,
                    image=img,
                    is_primary=(i == 0)
                )

            messages.success(request, f'Property "{property_obj.title}" has been added successfully!')
            return redirect('admin_properties')
    else:
        form = PropertyForm()

    return render(request, 'dashboard/admin/property_form.html', {'form': form, 'editing': False})


@admin_required
def admin_property_edit(request, pk):
    """Edit an existing property."""
    property_obj = get_object_or_404(Property, pk=pk)

    if request.method == 'POST':
        form = PropertyForm(request.POST, instance=property_obj)
        images = request.FILES.getlist('images')

        if form.is_valid():
            form.save()

            for img in images:
                PropertyImage.objects.create(
                    property=property_obj,
                    image=img,
                    is_primary=False
                )

            messages.success(request, f'Property "{property_obj.title}" has been updated!')
            return redirect('admin_properties')
    else:
        form = PropertyForm(instance=property_obj)

    existing_images = property_obj.images.all()
    context = {
        'form': form,
        'editing': True,
        'property': property_obj,
        'existing_images': existing_images,
    }
    return render(request, 'dashboard/admin/property_form.html', context)


@admin_required
def admin_property_delete(request, pk):
    """Delete a property."""
    property_obj = get_object_or_404(Property, pk=pk)
    if request.method == 'POST':
        title = property_obj.title
        property_obj.delete()
        messages.success(request, f'Property "{title}" has been deleted.')
    return redirect('admin_properties')


@admin_required
def admin_property_image_delete(request, pk):
    """Delete a property image."""
    image = get_object_or_404(PropertyImage, pk=pk)
    property_pk = image.property.pk
    image.delete()
    messages.success(request, 'Image deleted.')
    return redirect('admin_property_edit', pk=property_pk)


@admin_required
def admin_users(request):
    """Manage customer accounts."""
    users = CustomUser.objects.filter(role='customer').order_by('-date_joined')

    search = request.GET.get('search')
    if search:
        users = users.filter(
            Q(username__icontains=search) |
            Q(email__icontains=search) |
            Q(first_name__icontains=search) |
            Q(last_name__icontains=search)
        )

    paginator = Paginator(users, 10)
    page = request.GET.get('page')
    users = paginator.get_page(page)

    context = {'users': users, 'search': search or ''}
    return render(request, 'dashboard/admin/users.html', context)


@admin_required
def admin_toggle_user(request, pk):
    """Activate/deactivate a user account."""
    user = get_object_or_404(CustomUser, pk=pk)
    if request.method == 'POST':
        user.is_active = not user.is_active
        user.save()
        status = 'activated' if user.is_active else 'deactivated'
        messages.success(request, f'User "{user.username}" has been {status}.')
    return redirect('admin_users')


@admin_required
def admin_transactions(request):
    """View and manage transactions."""
    transactions = Transaction.objects.all()

    status = request.GET.get('status')
    if status:
        transactions = transactions.filter(status=status)

    paginator = Paginator(transactions, 10)
    page = request.GET.get('page')
    transactions = paginator.get_page(page)

    context = {'transactions': transactions, 'current_status': status}
    return render(request, 'dashboard/admin/transactions.html', context)


@admin_required
def admin_transaction_update(request, pk):
    """Update transaction status."""
    transaction = get_object_or_404(Transaction, pk=pk)
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in dict(Transaction.STATUS_CHOICES):
            old_status = transaction.status
            transaction.status = new_status
            transaction.transaction_date = timezone.now()  # ✅ refresh date
            transaction.save()

            # Update property status based on transaction status
            if new_status == 'completed':
                transaction.listing.status = 'sold'
                transaction.listing.save()
            elif new_status == 'approved':
                transaction.listing.status = 'reserved'
                transaction.listing.save()
            elif new_status == 'cancelled':
                transaction.listing.status = 'available'
                transaction.listing.save()
            elif new_status == 'pending':
                transaction.listing.status = 'available'
                transaction.listing.save()

            messages.success(request, f'Transaction #{transaction.pk} updated to {new_status}.')

    # ✅ Preserve the status filter after redirect
    status_filter = request.POST.get('current_status', '')
    if status_filter:
        return redirect(f'/dashboard/admin/transactions/?status={status_filter}')
    return redirect('admin_transactions')


@admin_required
def admin_inquiries(request):
    """View and reply to inquiries."""
    inquiries = Inquiry.objects.all()

    status = request.GET.get('status')
    if status:
        inquiries = inquiries.filter(status=status)

    paginator = Paginator(inquiries, 10)
    page = request.GET.get('page')
    inquiries = paginator.get_page(page)

    context = {'inquiries': inquiries, 'current_status': status}
    return render(request, 'dashboard/admin/inquiries.html', context)


@admin_required
def admin_inquiry_reply(request, pk):
    """Reply to a customer inquiry."""
    inquiry = get_object_or_404(Inquiry, pk=pk)

    if request.method == 'POST':
        form = InquiryReplyForm(request.POST, instance=inquiry)
        if form.is_valid():
            inquiry = form.save(commit=False)
            inquiry.status = 'replied'
            inquiry.save()
            messages.success(request, 'Reply sent successfully!')
    return redirect('admin_inquiries')


@admin_required
def admin_reports(request):
    """Sales and property analytics/reports."""
    # Total revenue
    total_revenue = Transaction.objects.filter(status='completed').aggregate(
        total=Sum('amount')
    )['total'] or 0

    # Monthly sales
    monthly_sales = (
        Transaction.objects
        .filter(status='completed')
        .annotate(month=TruncMonth('transaction_date'))
        .values('month')
        .annotate(total=Sum('amount'), count=Count('id'))
        .order_by('month')
    )

    # Property stats
    total_properties = Property.objects.count()
    available_count = Property.objects.filter(status='available').count()
    sold_count = Property.objects.filter(status='sold').count()
    reserved_count = Property.objects.filter(status='reserved').count()

    # Type breakdown
    type_breakdown = (
        Property.objects
        .values('property_type')
        .annotate(count=Count('id'))
        .order_by('-count')
    )

    # Customer activity
    active_customers = CustomUser.objects.filter(role='customer', is_active=True).count()
    total_inquiries = Inquiry.objects.count()
    total_favorites = Favorite.objects.count()

    context = {
        'total_revenue': total_revenue,
        'monthly_sales': list(monthly_sales),
        'total_properties': total_properties,
        'available_count': available_count,
        'sold_count': sold_count,
        'reserved_count': reserved_count,
        'type_breakdown': list(type_breakdown),
        'active_customers': active_customers,
        'total_inquiries': total_inquiries,
        'total_favorites': total_favorites,
    }
    return render(request, 'dashboard/admin/reports.html', context)


# ─────────────────────────────────────────────
# CUSTOMER DASHBOARD VIEWS
# ─────────────────────────────────────────────

@customer_required
def customer_dashboard(request):
    """Customer overview dashboard."""
    favorites_count = Favorite.objects.filter(customer=request.user).count()
    inquiries_count = Inquiry.objects.filter(customer=request.user).count()
    purchases = Transaction.objects.filter(customer=request.user)
    pending_purchases = purchases.filter(status='pending').count()
    completed_purchases = purchases.filter(status='completed').count()

    recent_favorites = Favorite.objects.filter(customer=request.user)[:4]
    recent_inquiries = Inquiry.objects.filter(customer=request.user)[:5]

    context = {
        'favorites_count': favorites_count,
        'inquiries_count': inquiries_count,
        'pending_purchases': pending_purchases,
        'completed_purchases': completed_purchases,
        'recent_favorites': recent_favorites,
        'recent_inquiries': recent_inquiries,
    }
    return render(request, 'dashboard/customer/index.html', context)


@customer_required
def customer_favorites(request):
    """Customer's saved/favorite properties."""
    favorites = Favorite.objects.filter(customer=request.user).select_related('property')

    paginator = Paginator(favorites, 9)
    page = request.GET.get('page')
    favorites = paginator.get_page(page)

    return render(request, 'dashboard/customer/favorites.html', {'favorites': favorites})


@customer_required
def customer_inquiries(request):
    """Customer's sent inquiries and replies."""
    inquiries = Inquiry.objects.filter(customer=request.user)

    paginator = Paginator(inquiries, 10)
    page = request.GET.get('page')
    inquiries = paginator.get_page(page)

    return render(request, 'dashboard/customer/inquiries.html', {'inquiries': inquiries})


@customer_required
def customer_purchases(request):
    """Customer's purchase/reservation tracking."""
    transactions = Transaction.objects.filter(customer=request.user)

    status = request.GET.get('status')
    if status:
        transactions = transactions.filter(status=status)

    paginator = Paginator(transactions, 10)
    page = request.GET.get('page')
    transactions = paginator.get_page(page)

    return render(request, 'dashboard/customer/purchases.html', {
        'transactions': transactions,
        'current_status': status,
    })
from django.contrib.auth.decorators import login_required

@login_required
def buy_property(request, pk):
    property_obj = get_object_or_404(Property, pk=pk)
    if request.method == 'POST':
        payment_method = request.POST.get('payment_method')
        notes = request.POST.get('notes', '')
        Transaction.objects.create(
            listing=property_obj,
            customer=request.user,
            amount=property_obj.price,
            payment_method=payment_method,
            notes=notes,
            status='pending'
        )
        property_obj.status = 'reserved'
        property_obj.save()
        messages.success(request, 'Purchase request submitted! Waiting for admin approval.')
    return redirect('property_detail', pk=pk)
