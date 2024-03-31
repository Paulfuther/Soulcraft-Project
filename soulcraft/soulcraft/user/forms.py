from django import forms


class TwoFactorAuthenticationForm(forms.Form):
    verification_code = forms.CharField(
        max_length=12,
        required=True,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )

    def __init__(self, *args, **kwargs):
        super(TwoFactorAuthenticationForm, self).__init__(*args, **kwargs)
        self.fields["verification_code"].widget.attrs.update(
            {"style": "margin: 10px 0;"}
        )
