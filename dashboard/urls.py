from django.urls import path
from . import views

urlpatterns = [
    # Admin Dashboard
    path('admin/', views.admin_dashboard, name='admin_dashboard'),
    path('admin/properties/', views.admin_properties, name='admin_properties'),
    path('admin/properties/add/', views.admin_property_add, name='admin_property_add'),
    path('admin/properties/<int:pk>/edit/', views.admin_property_edit, name='admin_property_edit'),
    path('admin/properties/<int:pk>/delete/', views.admin_property_delete, name='admin_property_delete'),
    path('admin/properties/image/<int:pk>/delete/', views.admin_property_image_delete, name='admin_property_image_delete'),
    path('admin/users/', views.admin_users, name='admin_users'),
    path('admin/users/<int:pk>/toggle/', views.admin_toggle_user, name='admin_toggle_user'),
    path('admin/transactions/', views.admin_transactions, name='admin_transactions'),
    path('admin/transactions/<int:pk>/update/', views.admin_transaction_update, name='admin_transaction_update'),
    path('admin/inquiries/', views.admin_inquiries, name='admin_inquiries'),
    path('admin/inquiries/<int:pk>/reply/', views.admin_inquiry_reply, name='admin_inquiry_reply'),
    path('admin/reports/', views.admin_reports, name='admin_reports'),

    # Customer Dashboard
    path('customer/', views.customer_dashboard, name='customer_dashboard'),
    path('customer/favorites/', views.customer_favorites, name='customer_favorites'),
    path('customer/inquiries/', views.customer_inquiries, name='customer_inquiries'),
    path('customer/purchases/', views.customer_purchases, name='customer_purchases'),
]
