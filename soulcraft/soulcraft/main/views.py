from django.contrib import messages
from django.shortcuts import redirect, render

from soulcraft.msg.helpers import create_single_email

from soulcraft.forms import ContactForm


def _handle_contact_post(request, redirect_name, topic_default=None):
    form = ContactForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        data = form.cleaned_data
        if topic_default and not data.get("topic"):
            data["topic"] = topic_default
        try:
            print("data :", data)
            create_single_email(data)
            messages.success(request, "Thanks — we’ll get back to you shortly.")
        except Exception as e:
            messages.error(request, f"Sorry, your message could not be sent. ({e})")
        return redirect(redirect_name)
    return form


def home(request):
    form = _handle_contact_post(request, "home")
    return render(request, "main/home.html", {"form": form})


def services(request):
    form = _handle_contact_post(request, "services", topic_default="services")
    return render(request, "main/services.html", {"form": form})


def platform(request):
    form = _handle_contact_post(request, "platform", topic_default="platform")
    return render(request, "main/platform.html", {"form": form})
