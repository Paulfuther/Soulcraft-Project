from django.contrib import admin

from soulcraft.error_logging.models import ErrorLog


@admin.register(ErrorLog)
class ErrorLogAdmin(admin.ModelAdmin):
    list_display = ("timestamp", "status_code", "path", "method")
    list_filter = ("status_code", "timestamp", "method")
    search_fields = ("path",)
