from django import forms


class VerifyEmailForm(forms.Form):
    email = forms.EmailField(
        max_length=254, help_text="Required to fetch username.")
