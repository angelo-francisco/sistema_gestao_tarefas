from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import PasswordResetCode


class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

    def clean_email(self):
        email = self.cleaned_data.get("email")

        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email was already registered!")

        return email


class ForgotPasswordForm(forms.Form):
    RESET_CHOICES = [
        ('email', 'Link de redefinição'),
        ('code', 'Código de redefinição'),
    ]

    email = forms.EmailField(
        label="Email",
        help_text="Enter the email address associated with your account. Make sure it is valid and accessible.",
        required=True,
    )

    reset_method = forms.ChoiceField(
        choices=RESET_CHOICES, 
        widget=forms.RadioSelect, 
        label="Selecione o método para redefinir sua senha",
        required=True
    )

    def clean_reset_method(self):
        reset_method = self.cleaned_data.get("reset_method")
        
        if reset_method not in ('email', 'code'):
            raise forms.ValidationError("Reset Method not Allowed")
        
        return reset_method

    def clean_email(self):
        email = self.cleaned_data.get("email")

        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is not registered in our system.")

        return email

    def get_user(self):
        email = self.cleaned_data.get("email")
        try:
            user = User.objects.get(email=email)
            return user
        except User.DoesNotExist:
            return None


class VerifyCodeForm(forms.Form):
    code = forms.CharField(
        label="",
        widget=forms.TextInput(
            {   
                "maxlength": "8",
                "id": "pin",
                "pattern": "[A-Za-z0-9]{8}",
                "placeholder": "Enter 8 digits/letters",
                "title": "Only 8 alphanumeric characters are allowed"
            }
        )
    )

    def clean_code(self):
        code = self.cleaned_data.get("code")

        if not PasswordResetCode.objects.filter(code=code).exists():
            raise forms.ValidationError("Invalid Code")
        return code