from django.contrib import admin
from django.contrib.admin import AdminSite
from django.contrib.auth.admin import GroupAdmin, UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group, User
from django.urls import path
from soulcraft.profiles.models import UserProfile
from soulcraft.error_logging.models import ErrorLog

from .views import custom_admin_view


class ErrorLogAdmin(admin.ModelAdmin):
    list_display = ("timestamp", "status_code", "path", "method")
    list_filter = ("status_code", "timestamp", "method")
    search_fields = ("path",)


class MyAdminSite(AdminSite):
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                "email-stats/", self.admin_view(custom_admin_view), name="email_stats"
            ),
        ]
        return custom_urls + urls


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'UserProfile'
    fk_name = 'user'


class UserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline, )

    list_display = ('username', 'email', 'first_name', 'last_name', 'get_phone_number', 'is_staff')

    def get_phone_number(self, instance):
        """
        This method returns the phone number for each user.
        If the user has no profile or phone number, it returns an empty string.
        """
        if hasattr(instance, 'userprofile'):
            return instance.userprofile.phone_number
        return ''

    get_phone_number.short_description = 'Phone Number'  # Sets column name


admin.site.unregister(User)
admin_site = MyAdminSite(name="myadmin")
admin_site.register(ErrorLog, ErrorLogAdmin)
admin_site.register(User, UserAdmin)
admin_site.register(Group, GroupAdmin)
