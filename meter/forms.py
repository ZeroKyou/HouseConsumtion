# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth.models import User
from django.core import validators
from meter.models import Settings


class SignupForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control',
                                               'placeholder': 'Nome de utilizador'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control',
                                                 'placeholder': 'Primeiro nome'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control',
                                                'placeholder': 'Último nome'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Correio Eletrónico'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control',
                                                   'placeholder': 'Palavra-chave'}),
        }
        labels = {
            'username': "Nome de utilizador:",
            'first_name': "Primeiro nome:",
            'last_name': "Último nome:",
            'email': "Correio eletrónico:",
            'password': "Palavra-chave:",
        }


class EditEmailForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(EditEmailForm, self).__init__(*args, **kwargs)
        self.fields['email'].required = True
        self.fields['email'].validators = [validators.EmailValidator(
            message="O correio eletrónico é de preenchimento obrigatório."
        )]

    class Meta:
        model = User
        fields = ('email',)
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Correio Eletrónico'})
        }
        labels = {
            'email': "Correio eletrónico:"
        }


class SettingsForm(forms.ModelForm):

    class Meta:
        model = Settings
        fields = ('cost_kw_per_hour', 'cost_m3', 'send_email', 'power_warning', 'liters_warning')
        widgets = {
            'cost_kw_per_hour': forms.NumberInput(attrs={'class': 'form-control',
                                                         'placeholder': 'Custo kW/h em euros'}),
            'cost_m3': forms.NumberInput(attrs={'class': 'form-control',
                                                'placeholder': 'Custo por metro cúbico em euros'}),
            'send_email': forms.CheckboxInput(),
            'power_warning': forms.NumberInput(attrs={'class': 'form-control',
                                                      'placeholder': 'Potência em Watts'}),
            'liters_warning': forms.NumberInput(attrs={'class': 'form-control',
                                                       'placeholder': 'Litros de água'}),
        }
        labels = {
            'cost_kw_per_hour': "Custo(€) por kW/h:",
            'cost_m3': "Custo(€) por m³:",
            'send_email': "Enviar alerta por email:",
            'power_warning': "Limite de potência (W):",
            'liters_warning': "Limite de água (L):",
        }

