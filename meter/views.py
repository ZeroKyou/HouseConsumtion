# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from meter.forms import SignupForm
from meter.db_to_charts_classes import ElectricityGraphData
from meter.models import Electricity, Settings

from django.http import HttpResponse


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


# !!!!!!!!!!!!!!!!!!!!! IMPORTANT !!!!!!!!!!!!!!!!!!!!!!!!!!!!
# INSTEAD OF CREATING 4 VIEWS FOR EACH GRAHP, CREATE ONE VIEW
# THAT RECEIVES THE AN ARGUMENT WITH THE GRAPH WE WANT TO DRAW
# !!!!!!!!!!!!!!!!!!!!! IMPORTANT !!!!!!!!!!!!!!!!!!!!!!!!!!!!
# def electricity_meter(request, time_length):
#     ...(database query)...
#     return render(request, 'energy_meter/energy_meter.html', {[database_data], graph_to_draw})
def electricity_meter(request, time_period):
    # cost_kw_h = 1
    # currency = '€'
    # if request.user.is_authenticated:
    #     settings = Settings.objects.filter(user=request.user)
    #     currency = None
    #     for setting in settings:
    #         currency = setting.currency
    #         cost_kw_h = setting.cost_kw_per_hour
    #
    # avg_current = Electricity.objects.get_avg_current(time_period)
    # avg_voltage = Electricity.objects.get_avg_voltage(time_period)
    # avg_power = Electricity.objects.get_avg_power(time_period)
    # cost = Electricity.objects.get_cost(cost_kw_h, time_period)
    # averages = {'avg_current': avg_current,
    #             'avg_voltage': avg_voltage,
    #             'avg_power': avg_power,
    #             'cost': cost}
    #
    # x_axis = {
    #     "type": "datetime",
    #     "labels": {"format": "{value:%Y-%m-%d}", "rotation": "45", "align": "left"},
    #     "dateTimeLabelFormats": {"month": "%e. %b", "year": "%b"}
    #     }
    #
    # return render(request, 'energy_meter/energy_meter.html', {'averages': averages,
    #                                                           'time_period': time_period,
    #                                                           'currency': currency})
    return render(request, 'energy_meter/energy_meter.html', {'time_period': time_period})


def electricity_values(request, time_period):
    data = ElectricityGraphData.get_data(time_period)
    return HttpResponse(data, content_type="application/json")


@csrf_exempt
def add_meter_reading(request):
    pass


def water_meter(request, time_period):
    data = []
    return render(request, 'water_meter/water_meter.html', {'data': data, 'time_period': time_period})


@csrf_exempt
def add_water_reading(request):
    pass


def total_consumption(request, time_period):
    data = []
    return render(request, 'total_consumption/total_consumption.html', {'data': data, 'time_period': time_period})
