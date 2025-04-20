from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.core.exceptions import ValidationError
from django.core.files.storage import default_storage

from authentication.utils import is_password_safe
from users.models import CustomUser

@login_required
def my_profile(request):
    if request.method == 'POST':
        user: CustomUser = request.user
        try:
            # Update basic fields
            username = request.POST.get('username')
            user.first_name = request.POST.get('first_name', '')
            user.last_name = request.POST.get('last_name', '')

            # Control username uniqueness prior to update
            if username and username != user.username:
                if CustomUser.objects.filter(username=username).exists():
                    raise ValidationError('Username already exists')
                user.username = username

            # Handle avatar upload
            if 'avatar' in request.FILES:
                uploaded_file = request.FILES['avatar']
                ext = uploaded_file.name.split('.')[-1]
                uploaded_file.name = f"{user.id}.{ext}"

                # Delete the old avatar if it exists and is different
                if user.avatar and default_storage.exists(user.avatar.name):
                    default_storage.delete(user.avatar.name)

                user.avatar = uploaded_file

            # Handle password change if provided
            current_password = request.POST.get('current_password')
            new_password1 = request.POST.get('new_password1')
            new_password2 = request.POST.get('new_password2')
            
            if current_password and new_password1 and new_password2:
                if not user.check_password(current_password):
                    raise ValidationError('Current password is incorrect')
                if new_password1 != new_password2:
                    raise ValidationError('New passwords do not match')
                if not is_password_safe(new_password1):
                    raise ValidationError('New password is not safe')
                user.set_password(new_password1)
                update_session_auth_hash(request, user)

            user.save()
            messages.success(request, 'Profile updated successfully')
        except ValidationError as e:
            messages.error(request, str(e))
        except Exception as e:
            messages.error(request, f'Error updating profile: {str(e)}')

    return render(request, 'profile.html')
