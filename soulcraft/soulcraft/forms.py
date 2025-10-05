from django import forms
from django.core.validators import EmailValidator


class ContactForm(forms.Form):
    name = forms.CharField(max_length=120, label="Your name")
    email = forms.EmailField(validators=[EmailValidator()], label="Email")
    subject = forms.CharField(max_length=150, label="Subject")
    message = forms.CharField(widget=forms.Textarea(attrs={"rows": 5}), label="Message")
    topic = forms.ChoiceField(
        choices=[
            ("services", "Carwash Services"),
            ("platform", "Platform / Demo"),
            ("general", "General"),
        ],
        required=False,
        label="Topic"
    )