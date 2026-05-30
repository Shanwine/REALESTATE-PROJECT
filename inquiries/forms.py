from django import forms
from .models import Inquiry


class InquiryForm(forms.ModelForm):
    """Form for submitting property inquiries."""

    class Meta:
        model = Inquiry
        fields = ['subject', 'message']
        widgets = {
            'subject': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Subject of your inquiry',
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Write your message here...',
            }),
        }


class InquiryReplyForm(forms.ModelForm):
    """Form for admin to reply to inquiries."""

    class Meta:
        model = Inquiry
        fields = ['admin_reply']
        widgets = {
            'admin_reply': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Type your reply...',
            }),
        }
