# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from meter.forms import SignupForm, SettingsForm, EditEmailForm
from meter.db_to_charts_classes import ElectricityGraphData, WaterGraphData
from meter.models import Electricity, Water, Settings
from django.http import HttpResponse


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
        user_settings = Settings.objects.filter(user=request.user).first()
        if user_settings is not None:
            data = ElectricityGraphData().get_data(time_period, user_settings.cost_kw_per_hour)
        else:
            data = ElectricityGraphData().get_data(time_period, 0)
    else:
        data = ElectricityGraphData().get_data(time_period, 0)
    return HttpResponse(data, content_type="application/json")


def water_meter(request, time_period):
    return render(request, 'water_meter/water_meter.html', {'time_period': time_period})


def water_values(request, time_period):
    if request.user.is_authenticated:
        user_settings = Settings.objects.filter(user=request.user).first()
        if user_settings is not None:
            data = WaterGraphData().get_data(time_period, user_settings.cost_m3)
        else:
            data = WaterGraphData().get_data(time_period, 0)
    else:
        data = WaterGraphData().get_data(time_period, 0)
    return HttpResponse(data, content_type="application/json")


@login_required()
def settings(request):
    user_settings = get_object_or_404(Settings, user=request.user)
    if request.method == "POST":
        form_settings = SettingsForm(request.POST, instance=user_settings)
        form_email = EditEmailForm(request.POST, instance=request.user)
        if form_settings.is_valid() and form_email.is_valid():
            form_settings.save()
            form_email.save()
            messages.success(request, "Configurações alteradas com sucesso!")
            return redirect('index')
    else:
        form_settings = SettingsForm(instance=user_settings)
        form_email = EditEmailForm(instance=request.user)
    return render(request, 'settings/settings.html', {'form_settings': form_settings, 'form_email': form_email})


@csrf_exempt
def add_meter_reading(request):
    if request.method == "POST":
        irms = request.method.POST['irms']
        water_cycles = request.method.POST['water_cycles']
        Electricity.objects.save_reading(irms)
        Water.objects.save_reading(water_cycles)
