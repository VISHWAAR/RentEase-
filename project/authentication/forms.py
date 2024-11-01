from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate

class CustomLoginForm(AuthenticationForm):
    def confirm_login_allowed(self, user):
        if not user.is_active:
            raise forms.ValidationError(
                "This account is inactive.",
                code='inactive',
            )
