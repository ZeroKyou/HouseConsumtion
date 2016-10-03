from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from meter.forms import SignupForm
from meter.db_to_charts_classes import ElectricityGraphData


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


# !!!!!!!!!!!!!!!!!!!!! IMPORTANT !!!!!!!!!!!!!!!!!!!!!!!!!!!!
# INSTEAD OF CREATING 4 VIEWS FOR EACH GRAHP, CREATE ONE VIEW
# THAT RECEIVES THE AN ARGUMENT WITH THE GRAPH WE WANT TO DRAW
# !!!!!!!!!!!!!!!!!!!!! IMPORTANT !!!!!!!!!!!!!!!!!!!!!!!!!!!!
# def electricity_meter(request, time_length):
#     ...(database query)...
#     return render(request, 'energy_meter/energy_meter.html', {[database_data], graph_to_draw})
def electricity_meter(request, time_period):
    data = ElectricityGraphData.get_data(time_period)

    if data is None:
        data = []

    chart = {"renderTo": "graph-container", "type": "line", "height": "500px"}
    title = {"text": 'Energia Consumida'}
    x_axis = {"title": {"text": ''}, "categories": data['date']}
    y_axis = {"title": {"text": 'Data'}}
    series = [
        {"name": 'Current (A)', "data": data['current']},
        {"name": 'Voltage (V)', "data": data['voltage']},
        {"name": 'Power (W)', "data": data['power']}
    ]

    return render(request, 'energy_meter/energy_meter.html', {'chart': chart,
                                                              'title': title,
                                                              'xAxis': x_axis,
                                                              'yAxis': y_axis,
                                                              'series': series})


@csrf_exempt
def add_electricity_reading(request):
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
