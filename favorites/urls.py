from django.urls import path
from . import views

urlpatterns = [
    path('toggle/<int:property_pk>/', views.toggle_favorite, name='toggle_favorite'),
]
