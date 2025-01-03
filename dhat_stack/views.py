from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.utils.encoding import iri_to_uri
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.http import require_http_methods


def index(request):
    return render(request, 'index.html')


@require_http_methods(['GET', 'POST'])
def login_view(request):
    if request.user.is_authenticated:
        return redirect('/')
    template_url = 'registration/login.html'
    partial_template = 'registration/_login-partial.html'
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            next_url = request.GET.get('next')
            if url_has_allowed_host_and_scheme(next_url, None):
                next_url = iri_to_uri(next_url)
            else:
                next_url = '/'
            response = HttpResponse(200)
            response['HX-Redirect'] = next_url
            return response
        else:
            ctx = {"error": "Incorrect Credentials.", 'username': username, 'password': password}
            return render(request, partial_template, ctx)

    # GET
    if request.htmx:
        return render(request, partial_template)
    return render(request, template_url)


@require_http_methods(['POST', 'GET'])
def signup_view(request):
    if request.user.is_authenticated:
        return redirect('/')
    template_url = 'registration/signup.html'
    partial_template = 'registration/_signup-partial.html'
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = None
        error = None
        try:
            user = User.objects.create_user(username=username, password=password)
        except IntegrityError:
            error = "User with this username already exists"
        except:
            error = "Somthing went wrong"
        if user is not None:
            login(request, user)
            next_url = request.GET.get('next')
            if url_has_allowed_host_and_scheme(next_url, None):
                next_url = iri_to_uri(next_url)
            else:
                next_url = '/'
            response = HttpResponse(200)
            response['HX-Redirect'] = next_url
            return response
        ctx = {"error": error, "username": username, password: 'password'}
        return render(request, partial_template, ctx)

    # GET
    if request.htmx:
        return render(request, partial_template)
    return render(request, template_url)


def logout_action(request):
    logout(request)
    return redirect('/')
