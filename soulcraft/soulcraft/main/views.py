import logging

import requests
from django.conf import settings
from django.contrib import messages
from django.http.response import HttpResponseBase
from django.shortcuts import redirect, render

from soulcraft.forms import ContactForm
from soulcraft.msg.helpers import create_single_email


logger = logging.getLogger(__name__)


def _verify_turnstile(request):
    token = request.POST.get("cf-turnstile-response")

    if not token:
        return False

    try:
        response = requests.post(
            "https://challenges.cloudflare.com/turnstile/v0/siteverify",
            data={
                "secret": settings.TURNSTILE_SECRET_KEY,
                "response": token,
                "remoteip": request.META.get("REMOTE_ADDR"),
            },
            timeout=10,
        )

        response.raise_for_status()
        result = response.json()

        if not result.get("success"):
            logger.warning(
                "Turnstile verification failed: %s",
                result.get("error-codes", []),
            )

        return result.get("success", False)

    except (requests.RequestException, ValueError) as exc:
        logger.exception("Turnstile verification error: %s", exc)
        return False


def _handle_contact_post(request, redirect_name, topic_default=None):
    form = ContactForm(request.POST or None)

    if request.method != "POST":
        return form

    if not form.is_valid():
        return form

    if not _verify_turnstile(request):
        messages.error(
            request,
            "Please complete the security verification and try again.",
        )
        return form

    data = form.cleaned_data.copy()

    if topic_default and not data.get("topic"):
        data["topic"] = topic_default

    try:
        email_sent = create_single_email(data)

        if email_sent:
            messages.success(
                request,
                "Thanks — we’ll get back to you shortly.",
            )
        else:
            messages.error(
                request,
                "Sorry, your message could not be sent. Please try again.",
            )

    except Exception:
        logger.exception("Contact form email error")

        messages.error(
            request,
            "Sorry, your message could not be sent. Please try again.",
        )

    return redirect(redirect_name)


def home(request):
    result = _handle_contact_post(request, "home")

    if isinstance(result, HttpResponseBase):
        return result

    return render(
        request,
        "main/home.html",
        {
            "form": result,
            "turnstile_site_key": settings.TURNSTILE_SITE_KEY,
        },
    )


def services(request):
    result = _handle_contact_post(
        request,
        "services",
        topic_default="services",
    )

    if isinstance(result, HttpResponseBase):
        return result

    return render(
        request,
        "main/services.html",
        {
            "form": result,
            "turnstile_site_key": settings.TURNSTILE_SITE_KEY,
        },
    )


def platform(request):
    result = _handle_contact_post(
        request,
        "platform",
        topic_default="platform",
    )

    if isinstance(result, HttpResponseBase):
        return result

    return render(
        request,
        "main/platform.html",
        {
            "form": result,
            "turnstile_site_key": settings.TURNSTILE_SITE_KEY,
        },
    )