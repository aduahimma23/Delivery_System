from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser
from django import forms

class CustomUserCreationForm(UserCreationForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'}), label="")
    terms_and_conditions = forms.BooleanField(label="I agree to the terms and conditions")

    class Meta:
        model = CustomUser
        fields = ("email", "password1", "password2", "confirm_password", "terms_and_conditions")
        widgets = {
            'email': forms.EmailInput(attrs={'placeholder': 'Email'}),
            'password1': forms.PasswordInput(attrs={'placeholder': 'Password'}),
            'password2': forms.PasswordInput(attrs={'placeholder': 'Confirm Password'}),
        }


    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        confirm_password = cleaned_data.get("confirm_password")
        terms_and_conditions = cleaned_data.get("terms_and_conditions")

        if password1 and password1 != confirm_password:
            self.add_error('confirm_password', "Passwords do not match")

        if not terms_and_conditions:
            self.add_error('terms_and_conditions', "You must agree to the terms and conditions to register.")

class LoginForm(AuthenticationForm):
    class Meta:
        model = CustomUser
        fields = ['email', 'password']
