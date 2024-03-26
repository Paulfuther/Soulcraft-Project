from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import FormView

from soulcraft.tasks import send_email_task

from .forms import ContactForm


class HomePageView(FormView):
    template_name = "main/welcome.html"
    form_class = ContactForm
    success_url = reverse_lazy("home")  # Redirect to home page upon success

    def form_valid(self, form):
        to_email = form.cleaned_data["to_email"]
        body = form.cleaned_data["body"]

        send_email_task.delay(to_email, body)

        messages.success(self.request, "Thank you for your enquiry!")

        return super().form_valid(form)
