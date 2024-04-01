from django.contrib import admin
from django.urls import include, path

from soulcraft.user.views import CustomAdminLoginView
from soulcraft.user.admin import admin_site

admin.site.login = CustomAdminLoginView.as_view()

urlpatterns = [
    path("admin/", admin_site.urls),
    path("", include("soulcraft.main.urls")),
    path("", include("soulcraft.msg.urls")),
    path("", include("soulcraft.user.urls")),
    path(
        "custom-admin-login/", CustomAdminLoginView.as_view(), name="custom_admin_login"
    ),
]


handler403 = "soulcraft.views.error_403"
handler500 = "soulcraft.views.error_500"
handler404 = "soulcraft.views.error_404"
