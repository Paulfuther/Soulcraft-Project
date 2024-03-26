from django.urls import path
from .views import fetch_sendgrid_events

urlpatterns = [
    path('api/sendgrid/events/', fetch_sendgrid_events, name='fetch_sendgrid_events'),
]
