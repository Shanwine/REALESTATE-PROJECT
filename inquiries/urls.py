from django.urls import path
from . import views

urlpatterns = [
    path('send/', views.send_inquiry, name='send_inquiry'),
    path('send/<int:property_pk>/', views.send_inquiry, name='send_property_inquiry'),
]
