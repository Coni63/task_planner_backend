from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, authenticate, login
from django.contrib import messages
from django.contrib.auth import get_user_model
from django import forms

from .utils import is_password_safe
from .forms import LoginForm, RegisterForm

User = get_user_model()


def login_user(request):
    if request.user.is_authenticated:
        return redirect('home')

    form = LoginForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            remember = form.cleaned_data['remember']

            user = authenticate(request, username=username, password=password)
            if user is not None:
                if not remember:
                    request.session.set_expiry(0)  # Session expires on browser close
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, 'Invalid username or password')

    return render(request, 'login.html', {'form': form})


def register_user(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            User = get_user_model()
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                first_name=form.cleaned_data['firstname'],
                last_name=form.cleaned_data['lastname'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password1']
            )
            login(request, user)
            messages.success(request, 'Account created successfully!')
            return redirect('home')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = RegisterForm()

    return render(request, 'register.html', {'form': form})


@login_required
def logout_user(request):
    logout(request)
    return render(request, 'home.html')