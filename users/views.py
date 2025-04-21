from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from users.forms import CustomUserForm
from users.models import CustomUser, Role


@login_required
def profile(request, pk):
    profile_user = get_object_or_404(CustomUser, pk=pk)
    is_self = profile_user.id == request.user.id
    is_admin = request.user.role == Role.ADMIN.value

    if request.method == 'POST' and is_self:
        form = CustomUserForm(request.POST, request.FILES, instance=profile_user, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated!')
    else:
        form = CustomUserForm(instance=profile_user, user=request.user)

    template = 'profile.html' if is_self else 'profile-ro.html'
    return render(request, template, {
        'form': form,
        'profile_user': profile_user,
        'is_self': is_self,
        'is_admin': is_admin,
    })