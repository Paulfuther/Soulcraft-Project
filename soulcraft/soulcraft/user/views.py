import logging

from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from twilio.base.exceptions import TwilioException, TwilioRestException

from soulcraft.msg.helpers import check_verification_token, request_verification_token
from soulcraft.profiles.models import UserProfile

from .forms import TwoFactorAuthenticationForm

logger = logging.getLogger(__name__)


def request_verification(request):
    if request.method == "POST":
        phone_number = request.POST.get("phone_number")
        print("Phone number:", phone_number)  # Debugging statement
        try:
            # Request the verification code from Twilio
            request_verification_token(phone_number)
            # Verification request successful
            # Return a success response
            return JsonResponse({"success": True})
        except TwilioException:
            # Handle TwilioException if verification request fails
            return JsonResponse(
                {"success": False, "error": "Failed to send verification code"}
            )
    # Return an error response for unsupported request methods
    return JsonResponse({"success": False, "error": "Invalid request method"})


def check_verification(request):
    if request.method == "POST":
        phone = request.POST.get("phone_number")
        token = request.POST.get("verification_code")
        print("Phone number:", phone)
        print("Verification code:", token)
        print(phone, token)
        try:
            if check_verification_token(phone, token):
                return JsonResponse({"success": True})
        except TwilioException:
            return JsonResponse(
                {"success": False, "error": "Failed to send verification code"}
            )
    return JsonResponse({"success": False, "error": "Invalid request method"})


def admin_verification_page(request):
    form = TwoFactorAuthenticationForm(request.POST)
    user_id = request.session.get("user_id", None)
    if not user_id:
        return HttpResponse(
            "User information not found in session. Please start the process again."
        )
    try:
        user = User.objects.get(id=user_id)
        print(user.username)
    except User.DoesNotExist:
        return HttpResponse("User not found.")

    if request.method == "POST":
        token = request.POST.get("verification_code")
        phone_number = request.session.get("phone_number", None)

        print("testing", token, phone_number)
        try:
            if check_verification_token(phone_number, token):
                login(request, user)
                return redirect("admin:index")
            else:
                return render(
                    request,
                    "user/admin_verification_page.html",
                    {"verification_error": True, "form": form},
                )
        except TwilioException:
            return render(
                request,
                "user/admin_verification_page.html",
                {"verification_error": True, "form": form},
            )

    return render(request, "user/admin_verification_page.html", {"form": form})


class CustomAdminLoginView(LoginView):
    template_name = "registration/login.html"
    form_class = AuthenticationForm

    def form_invalid(self, form):
        messages.error(self.request, "Invalid username or password.")
        return super().form_invalid(form)

    def form_valid(self, form):
        user = form.get_user()
        user_profile = self.get_user_profile(user)
        if user_profile and user_profile.phone_number:
            return self.handle_2fa(user, user_profile)
        # If 2FA is not required or setup, proceed to admin dashboard.
        return redirect("admin:index")

    def get_user_profile(self, user):
        try:
            return UserProfile.objects.get(user=user)
        except UserProfile.DoesNotExist:
            messages.error(self.request, "User profile does not exist.")
            return None

    def handle_2fa(self, user, user_profile):
        try:
            request_verification_token(user_profile.phone_number)
            self.request.session["user_id"] = user.id
            self.request.session["phone_number"] = user_profile.phone_number
            return redirect("admin_verification_page")
        except TwilioRestException as e:
            # Log the error for debugging purposes
            logger.error(f"Twilio error: {e}")
            # Inform the user of the error and suggest possible actions
            messages.error(
                self.request,
                "We encountered an error sending the verification code. Please try again later.",
            )
            return redirect(reverse("custom_admin_login"))
