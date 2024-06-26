from django.contrib import admin

# from django.contrib.admin import AdminSite
from django.contrib.auth.admin import GroupAdmin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group, User

from soulcraft.error_logging.models import ErrorLog

# from django.urls import path
from soulcraft.profiles.models import UserProfile

# from .views import custom_admin_view
# custom admin view was for email stats from sendgrid.
# I am not going to do this inthe admin. Not right now.


class ErrorLogAdmin(admin.ModelAdmin):
    list_display = ("timestamp", "status_code", "path", "method")
    list_filter = ("status_code", "timestamp", "method")
    search_fields = ("path",)


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = "UserProfile"
    fk_name = "user"


class UserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline,)

    list_display = (
        "username",
        "email",
        "first_name",
        "last_name",
        "get_phone_number",
        "is_staff",
    )

    def get_phone_number(self, instance):
        """
        This method returns the phone number for each user.
        If the user has no profile or phone number, it returns an empty string.
        """
        if hasattr(instance, "userprofile"):
            return instance.userprofile.phone_number
        return ""

    get_phone_number.short_description = "Phone Number"  # Sets column name


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.register(ErrorLog, ErrorLogAdmin)
admin.register(Group, GroupAdmin)
