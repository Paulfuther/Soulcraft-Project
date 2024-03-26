from django.contrib import admin
from django.urls import include, path


urlpatterns = [
    path("admin/", admin.site.urls),
    path('', include('soulcraft.main.urls')),
    path('', include('soulcraft.msg.urls')),
]
