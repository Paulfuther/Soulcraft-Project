from django import forms

class ContactForm(forms.Form):
    to_email = forms.EmailField(label="Your Email")
    body = forms.CharField(widget=forms.Textarea, label="Comments or Questions")