from django.urls import path

from .views import admin_verification_page

urlpatterns = [
    path(
        "admin_verification/", admin_verification_page, name="admin_verification_page"
    ),
]
