from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Inquiry
from .forms import InquiryForm
from properties.models import Property


@login_required
def send_inquiry(request, property_pk=None):
    """Send an inquiry about a property."""
    property_obj = None
    if property_pk:
        property_obj = get_object_or_404(Property, pk=property_pk)

    if request.method == 'POST':
        form = InquiryForm(request.POST)
        if form.is_valid():
            inquiry = form.save(commit=False)
            inquiry.customer = request.user
            inquiry.property = property_obj
            inquiry.save()
            messages.success(request, 'Your inquiry has been sent successfully!')
            if property_obj:
                return redirect('property_detail', pk=property_obj.pk)
            return redirect('customer_inquiries')
    else:
        initial = {}
        if property_obj:
            initial['subject'] = f"Inquiry about: {property_obj.title}"
        form = InquiryForm(initial=initial)

    context = {
        'form': form,
        'property': property_obj,
    }
    return render(request, 'inquiries/inquiry_form.html', context)
