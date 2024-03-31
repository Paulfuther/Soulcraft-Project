from django.urls import path

from .views import fetch_sendgrid_events, fetch_sendgrid_stats, fetch_sendgrid_messages

urlpatterns = [
    path("api/sendgrid/events/", fetch_sendgrid_events, name="fetch_sendgrid_events"),
    path("fetch-stats/", fetch_sendgrid_stats, name="fetch_sendgrid_stats"),
    path("fetch-emails/", fetch_sendgrid_messages, name="fetch_sendgrid_messages")
]
