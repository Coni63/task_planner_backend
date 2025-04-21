from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from .utils import is_password_safe


User = get_user_model()

class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'placeholder': 'Enter your username',
            'class': 'input input-bordered w-full',
            'id': 'id_username'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Enter your password',
            'class': 'input input-bordered w-full',
            'id': 'id_password'
        })
    )
    remember = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'checkbox checkbox-primary'
        })
    )


class RegisterForm(forms.Form):
    username = forms.CharField(max_length=150)
    firstname = forms.CharField(max_length=30)
    lastname = forms.CharField(max_length=150)
    email = forms.EmailField()
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match")

        if password1 and not is_password_safe(password1):
            raise forms.ValidationError("Password is not safe")

        return cleaned_data

    def clean_username(self):
        username = self.cleaned_data["username"]
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Username already exists")
        return username

    def clean_email(self):
        email = self.cleaned_data["email"]
        if User.objects.filter(email=email).exists():
            raise ValidationError("Email already in use")
        return email