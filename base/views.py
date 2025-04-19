from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseNotAllowed
from django.contrib.auth.decorators import login_required


from django.shortcuts import render

def home(request):
    # Initial counter value in session
    if 'counter' not in request.session:
        request.session['counter'] = 0
    return render(request, 'home.html', {'counter': request.session['counter']})

def increment(request):
    if 'counter' not in request.session:
        request.session['counter'] = 0
    request.session['counter'] += 1
    request.session.modified = True
    return render(request, 'home.html', {'counter': request.session['counter']})

def decrement(request):
    if 'counter' not in request.session:
        request.session['counter'] = 0
    request.session['counter'] -= 1
    request.session.modified = True
    return render(request, 'home.html', {'counter': request.session['counter']})