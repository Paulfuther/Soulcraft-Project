from django.contrib import messages
from django.urls import reverse_lazy
# from django.utils.decorators import method_decorator
from django.views.generic import FormView
# from django_ratelimit.decorators import ratelimit

from soulcraft.msg.helpers import create_single_email
# from soulcraft.tasks import send_email_task

from .forms import ContactForm


# @method_decorator(ratelimit(key="ip", rate="5/s", method="GET"), name="dispatch")
class HomePageView(FormView):
    template_name = "main/welcome.html"
    form_class = ContactForm
    success_url = reverse_lazy("home")  # Redirect to home page upon success

    def form_valid(self, form):
        to_email = form.cleaned_data["to_email"]
        body = form.cleaned_data["body"]

        # send_email_task.delay(to_email, body)
        create_single_email(to_email, body)

        messages.success(self.request, "Thank you for your enquiry!")

        return super().form_valid(form)
