# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from meter.forms import SignupForm
from meter.db_to_charts_classes import ElectricityGraphData
from meter.models import Settings

from django.http import HttpResponse, HttpResponseNotFound


# Create your views here.
def index(request):
    return render(request, "./index.html", {})


def login_successful(request):
    if User.is_authenticated:
        messages.success(request, "Login efetuado com sucesso!")
    return redirect('index')


def logout_successful(request):
    if User.is_authenticated is not True:
        messages.success(request, "Terminou a sessão.")
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


def electricity_meter(request, time_period):
    return render(request, 'energy_meter/energy_meter.html', {'time_period': time_period})


def electricity_values(request, time_period):
    if request.user.is_authenticated:
        settings = Settings.objects.filter(user=request.user).first()
        if settings is not None:
            data = ElectricityGraphData().get_data(time_period, settings.cost_kw_per_hour)
        else:
            data = ElectricityGraphData().get_data(time_period, 0)
    else:
        data = ElectricityGraphData().get_data(time_period, 0)
    return HttpResponse(data, content_type="application/json")


@csrf_exempt
def add_meter_reading(request):
    pass


def water_meter(request, time_period):
    data = []
    return render(request, 'water_meter/water_meter.html', {'data': data, 'time_period': time_period})
