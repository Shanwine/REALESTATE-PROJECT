
from django.urls import path

from dashboard.views import buy_property
from . import views

urlpatterns = [
    path('', views.property_list, name='property_list'),
    path('<int:pk>/', views.property_detail, name='property_detail'), 
    path('property/<int:pk>/buy/', buy_property, name='buy_property'),
]