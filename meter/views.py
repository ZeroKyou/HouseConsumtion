from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from meter.forms import SignupForm


# Create your views here.
def index(request):
    return render(request, "./index.html", {})


def login_successful(request):
    if User.is_authenticated:
        messages.success(request, "Login efetuado com sucesso!")
    return redirect('index')


def logout_successful(request):
    if User.is_authenticated is not True:
        messages.success(request, "Terminou a sessao.")
    return redirect('index')


def signup(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(user.password)
            user.save()
            user = authenticate(username=user.username, password=request.POST['password'])
            login(request, user)
            messages.success(request, "Utilizador criado com sucesso")
            return redirect('index')
        else:
            messages.error(request, form.errors)
    form = SignupForm()
    return render(request, 'registration/signup.html', {'form': form})


def electricity_meter(request):
    pass


def water_meter(request):
    pass
