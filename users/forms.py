# forms.py
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth import password_validation
from authentication.utils import is_password_safe
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

CustomUser = get_user_model()


class CustomUserForm(forms.ModelForm):
    new_password = forms.CharField(
        label='New Password',
        widget=forms.PasswordInput,
        required=False,
        help_text='Leave blank if you don\'t want to change your password.',
    )
    confirm_password = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput,
        required=False,
    )

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'avatar', 'role', 'first_name', 'last_name', 'new_password', 'confirm_password']
        widgets = {
            'email': forms.EmailInput(attrs={'readonly': 'readonly'}),
            'avatar': forms.FileInput(attrs={'accept': 'image/*'}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')  # pass the current user from the view
        super().__init__(*args, **kwargs)

    def clean_username(self):
        username = self.cleaned_data['username']
        if username != self.user.username:
            if CustomUser.objects.filter(username=username).exists():
                raise forms.ValidationError('Username already exists.')
        return username

    def clean_new_password2(self):
        pw1 = self.cleaned_data.get("new_password1")
        pw2 = self.cleaned_data.get("new_password2")

        if pw1 or pw2:
            if pw1 != pw2:
                raise forms.ValidationError("New passwords do not match.")
            password_validation.validate_password(pw1, self.user)
        return pw2

    def clean_avatar(self):
        avatar = self.cleaned_data.get('avatar')
        if "file" in avatar.__dict__:
            # ext = avatar.name.split('.')[-1]
            # avatar.name = f"{self.user.id}.{ext}"
            return avatar
        return None

    def save(self, commit=True):
        user = super().save(commit=False)

        # print(self.cleaned_data)

        # Rename avatar and delete old one
        new_avatar = self.cleaned_data.get('avatar')
        if new_avatar:
            user.avatar = new_avatar

        # Update password if changed
        new_password = self.cleaned_data.get("new_password2")
        if new_password:
            user.set_password(new_password)


        if commit:
            user.save()
        return user