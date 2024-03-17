from django.views.generic import FormView
from django.shortcuts import render
from .forms import ContactForm
from django.urls import reverse_lazy
from django.contrib import messages
from soulcraft.msg.helpers import create_single_email

class HomePageView(FormView):
    template_name = 'main/welcome.html'
    form_class = ContactForm
    success_url = reverse_lazy('home')  # Redirect to home page upon success

    def form_valid(self, form):
        to_email = form.cleaned_data['to_email']
        body = form.cleaned_data['body']

        if create_single_email(to_email, body):
            messages.success(self.request, "Email sent successfully!")
        else:
            messages.error(self.request, "Failed to send email.")

        return super().form_valid(form)
        
       

