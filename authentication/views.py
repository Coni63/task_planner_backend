from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

# Create your views here.
def login_user(request):
    context = {}
    return render(request, 'login.html', context)


def register_user(request):
    context = {}
    return render(request, 'register.html', context)

@login_required
def logout_user(request):
    logout(request)
    return render(request, 'home.html')