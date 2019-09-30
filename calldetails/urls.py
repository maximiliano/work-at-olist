"""calldetails URL Configuration"""

from django.urls import path
from core import views

urlpatterns = [
    path('calls/', views.calls),
]
